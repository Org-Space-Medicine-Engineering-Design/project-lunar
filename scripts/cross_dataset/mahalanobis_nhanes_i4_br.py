#!/usr/bin/env python3
"""
Mahalanobis distance bootstrap analysis for LUNAR NHANES vs Inspiration4 / Bed Rest overlap biomarkers.

Inputs expected in the same directory by default:
  - nhanes_biopro_all_cycles_combined.csv
  - LUNAR_Inspiration4_OVERLAP_Summary_v1.xlsx
  - LUNAR_BedRest_Campaign1_OVERLAP_Summary_v3.xlsx

Outputs:
  - outputs/mahalanobis_i4_density.png
  - outputs/mahalanobis_br_density.png
  - outputs/mahalanobis_combined_violin.png
  - outputs/mahalanobis_distance_summary.xlsx
  - outputs/mahalanobis_long_results.csv
  - outputs/analysis_panel_used.csv
"""

from __future__ import annotations

import argparse
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.spatial.distance import mahalanobis
from scipy.linalg import pinvh
from scipy.stats import gaussian_kde

TRUE_17_VARIABLES = [
    "ALBUMIN",
    "ALKALINE PHOSPHATASE",
    "ALT",
    "AST",
    "BILIRUBIN; TOTAL",
    "CALCIUM",
    "CARBON DIOXIDE",
    "CHLORIDE",
    "CREATININE",
    "GLUCOSE",
    "POTASSIUM",
    "PROTEIN; TOTAL",
    "SODIUM",
    "BUN",
    "GLOBULIN",
    "ALBUMIN/GLOBULIN RATIO",
    "BUN/CREATININE RATIO",
]

# NHANES variable map uses conventional/US-unit chemistry fields where possible.
NHANES_MAP = {
    "ALBUMIN": "LBXSAL",
    "ALKALINE PHOSPHATASE": "LBXSAPSI",
    "ALT": "LBXSATSI",
    "AST": "LBXSASSI",
    "BILIRUBIN; TOTAL": "LBXSTB",
    "CALCIUM": "LBXSCA",
    "CARBON DIOXIDE": "LBXSC3SI",
    "CHLORIDE": "LBXSCLSI",
    "CREATININE": "LBXSCR",
    "GLUCOSE": "LBXSGL",
    "POTASSIUM": "LBXSKSI",
    "PROTEIN; TOTAL": "LBXSTP",
    "SODIUM": "LBXSNASI",
    "BUN": "LBXSBU",
    "GLOBULIN": "LBXSGB",
}

NHANES_SECOND_DAY_MAP = {
    "ALBUMIN": "LB2SAL",
    "ALKALINE PHOSPHATASE": "LB2SAPSI",
    "ALT": "LB2SATSI",
    "AST": "LB2SASSI",
    "BILIRUBIN; TOTAL": "LB2STB",
    "CALCIUM": "LB2SCA",
    "CARBON DIOXIDE": "LB2SC3SI",
    "CHLORIDE": "LB2SCLSI",
    "CREATININE": "LB2SCR",
    "GLUCOSE": "LB2SGL",
    "POTASSIUM": "LB2SKSI",
    "PROTEIN; TOTAL": "LB2STP",
    "SODIUM": "LB2SNASI",
    "BUN": "LB2SBU",
}

SKEWED_VARS = {
    "ALKALINE PHOSPHATASE",
    "ALT",
    "AST",
    "BILIRUBIN; TOTAL",
    "CREATININE",
    "GLUCOSE",
    "BUN",
    "BUN/CREATININE RATIO",
}

I4_PRE_TIMEPOINTS = ["L-92", "L-44", "L-3"]
I4_POST_TIMEPOINTS = ["R+1", "R+45", "R+82", "R+194"]
BR_PHASES = ["PRE_TEST", "IN_TEST", "POST_TEST"]


def coalesce_columns(df: pd.DataFrame, primary: str | None, secondary: str | None = None) -> pd.Series:
    s = pd.Series(np.nan, index=df.index, dtype="float64")
    if primary and primary in df.columns:
        s = pd.to_numeric(df[primary], errors="coerce")
    if secondary and secondary in df.columns:
        s2 = pd.to_numeric(df[secondary], errors="coerce")
        s = s.combine_first(s2)
    return s


def load_nhanes(path: Path) -> pd.DataFrame:
    raw = pd.read_csv(path, low_memory=False)
    out = pd.DataFrame(index=raw.index)
    if "SEQN" in raw.columns:
        out["SEQN"] = raw["SEQN"]

    for var, col in NHANES_MAP.items():
        out[var] = coalesce_columns(raw, col, NHANES_SECOND_DAY_MAP.get(var))

    # Derived variables to match the overlap panel.
    out["ALBUMIN/GLOBULIN RATIO"] = out["ALBUMIN"] / out["GLOBULIN"]
    out["BUN/CREATININE RATIO"] = out["BUN"] / out["CREATININE"]

    # Basic biological plausibility filtering: positive only, because several variables are log-transformed.
    for var in TRUE_17_VARIABLES:
        out.loc[out[var] <= 0, var] = np.nan

    # One record per participant when SEQN exists. If duplicate rows have complementary values,
    # this keeps the first non-null value per variable per participant.
    if "SEQN" in out.columns:
        out = out.groupby("SEQN", as_index=False)[TRUE_17_VARIABLES].first()

    return out.dropna(subset=TRUE_17_VARIABLES).reset_index(drop=True)


def load_i4(path: Path) -> pd.DataFrame:
    df = pd.read_excel(path, sheet_name="Overlap_Data")
    df = df[df["Variable"].isin(TRUE_17_VARIABLES)].copy()
    df["Value"] = pd.to_numeric(df["Value"], errors="coerce")
    df = df.dropna(subset=["Subject_ID", "Timepoint", "Variable", "Value"])
    df["Analysis_Phase"] = np.where(df["Timepoint"].isin(I4_PRE_TIMEPOINTS), "Preflight",
                                     np.where(df["Timepoint"].isin(I4_POST_TIMEPOINTS), "Postflight", np.nan))
    df = df.dropna(subset=["Analysis_Phase"])

    # Average across the specified preflight/postflight timepoints within subject and variable.
    avg = df.groupby(["Subject_ID", "Analysis_Phase", "Variable"], as_index=False)["Value"].mean()
    wide = avg.pivot_table(index=["Subject_ID", "Analysis_Phase"], columns="Variable", values="Value", aggfunc="mean")
    wide = wide.reset_index()
    # Derive ratios from averaged components when the workbook ratio field is missing.
    if "ALBUMIN/GLOBULIN RATIO" not in wide.columns:
        wide["ALBUMIN/GLOBULIN RATIO"] = np.nan
    wide["ALBUMIN/GLOBULIN RATIO"] = wide["ALBUMIN/GLOBULIN RATIO"].fillna(wide["ALBUMIN"] / wide["GLOBULIN"])
    if "BUN/CREATININE RATIO" not in wide.columns:
        wide["BUN/CREATININE RATIO"] = np.nan
    wide["BUN/CREATININE RATIO"] = wide["BUN/CREATININE RATIO"].fillna(wide["BUN"] / wide["CREATININE"])
    return wide.dropna(subset=TRUE_17_VARIABLES).reset_index(drop=True)


def load_bedrest(path: Path) -> pd.DataFrame:
    df = pd.read_excel(path, sheet_name="Overlap_Data")
    # Harmonize the Bed Rest workbook BUN label to the 17-variable analysis panel.
    df["Inspiration4_Variable"] = df["Inspiration4_Variable"].replace({"UREA NITROGEN (BUN)": "BUN"})
    df = df[df["Inspiration4_Variable"].isin(TRUE_17_VARIABLES)].copy()
    df = df[df["Test_Phase"].isin(BR_PHASES)].copy()
    df["Value_Numeric"] = pd.to_numeric(df["Value_Numeric"], errors="coerce")
    df = df.dropna(subset=["Subject_ID", "Test_Phase", "Inspiration4_Variable", "Value_Numeric"])

    # Multiple measurements can exist per subject/phase/variable; average them to one vector per subject-phase.
    avg = df.groupby(["Subject_ID", "Test_Phase", "Inspiration4_Variable"], as_index=False)["Value_Numeric"].mean()
    wide = avg.pivot_table(index=["Subject_ID", "Test_Phase"], columns="Inspiration4_Variable", values="Value_Numeric", aggfunc="mean")
    phase_map = {"PRE_TEST": "Pre-BR", "IN_TEST": "In-BR", "POST_TEST": "Post-BR"}
    wide = wide.reset_index().rename(columns={"Test_Phase": "Analysis_Phase"})
    wide["Analysis_Phase"] = wide["Analysis_Phase"].map(phase_map)
    # Derive ratios from averaged components when needed.
    if "GLOBULIN" not in wide.columns:
        wide["GLOBULIN"] = wide["PROTEIN; TOTAL"] - wide["ALBUMIN"]
    if "ALBUMIN/GLOBULIN RATIO" not in wide.columns:
        wide["ALBUMIN/GLOBULIN RATIO"] = np.nan
    wide["ALBUMIN/GLOBULIN RATIO"] = wide["ALBUMIN/GLOBULIN RATIO"].fillna(wide["ALBUMIN"] / wide["GLOBULIN"])
    if "BUN/CREATININE RATIO" not in wide.columns:
        wide["BUN/CREATININE RATIO"] = np.nan
    wide["BUN/CREATININE RATIO"] = wide["BUN/CREATININE RATIO"].fillna(wide["BUN"] / wide["CREATININE"])
    return wide.dropna(subset=TRUE_17_VARIABLES).reset_index(drop=True)


def transform_and_standardize(nhanes: pd.DataFrame, i4: pd.DataFrame, br: pd.DataFrame):
    nh = nhanes[TRUE_17_VARIABLES].copy()
    i4_values = i4[TRUE_17_VARIABLES].copy()
    br_values = br[TRUE_17_VARIABLES].copy()

    for var in SKEWED_VARS:
        nh[var] = np.log(nh[var])
        i4_values[var] = np.log(i4_values[var])
        br_values[var] = np.log(br_values[var])

    mu = nh.mean(axis=0)
    sd = nh.std(axis=0, ddof=1).replace(0, np.nan)

    nh_z = (nh - mu) / sd
    i4_z = (i4_values - mu) / sd
    br_z = (br_values - mu) / sd

    if nh_z.isna().any().any() or i4_z.isna().any().any() or br_z.isna().any().any():
        raise ValueError("Missing or invalid values remain after transformation/standardization.")

    return nh_z.to_numpy(float), i4_z.to_numpy(float), br_z.to_numpy(float), mu, sd


def partition_indices(n: int, k: int, rng: np.random.Generator) -> list[np.ndarray]:
    idx = rng.permutation(n)
    return np.array_split(idx, k)


def md_from_ref(x: np.ndarray, centroid: np.ndarray, inv_cov: np.ndarray) -> float:
    return float(mahalanobis(x, centroid, inv_cov))


def run_bootstrap(nh_z, i4_meta, i4_z, br_meta, br_z, iterations: int, seed: int) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    records = []

    # Use a single NHANES covariance matrix for all bootstrap bins. This is much faster and
    # keeps the covariance structure stable while the bin centroids vary by resampling/splitting.
    full_cov = np.cov(nh_z, rowvar=False)
    full_cov = full_cov + np.eye(full_cov.shape[0]) * 1e-6
    inv_cov = pinvh(full_cov)

    i4_subjects = sorted(i4_meta["Subject_ID"].unique())
    br_subjects = sorted(br_meta["Subject_ID"].unique())
    if len(i4_subjects) != 4:
        raise ValueError(f"Expected 4 Inspiration4 subjects, found {len(i4_subjects)}: {i4_subjects}")
    if len(br_subjects) != 3:
        raise ValueError(f"Expected 3 Bed Rest subjects, found {len(br_subjects)}: {br_subjects}")

    i4_rows_by_subject = {s: i4_meta.index[i4_meta["Subject_ID"] == s].tolist() for s in i4_subjects}
    br_rows_by_subject = {s: br_meta.index[br_meta["Subject_ID"] == s].tolist() for s in br_subjects}

    for it in range(1, iterations + 1):
        # Inspiration4: split NHANES into 4 pseudo-reference bins, one per crew member.
        i4_bins = partition_indices(len(nh_z), 4, rng)
        for bin_number, (subj, bin_idx) in enumerate(zip(i4_subjects, i4_bins), start=1):
            centroid = nh_z[bin_idx, :].mean(axis=0)
            for row in i4_rows_by_subject[subj]:
                records.append({
                    "Iteration": it,
                    "Dataset": "Inspiration4",
                    "Subject_ID": i4_meta.loc[row, "Subject_ID"],
                    "Phase": i4_meta.loc[row, "Analysis_Phase"],
                    "NHANES_Bin": bin_number,
                    "Mahalanobis_Distance": md_from_ref(i4_z[row, :], centroid, inv_cov),
                })

        # Bed Rest: split NHANES into 3 pseudo-reference bins, one per confirmed subject.
        br_bins = partition_indices(len(nh_z), 3, rng)
        for bin_number, (subj, bin_idx) in enumerate(zip(br_subjects, br_bins), start=1):
            centroid = nh_z[bin_idx, :].mean(axis=0)
            for row in br_rows_by_subject[subj]:
                records.append({
                    "Iteration": it,
                    "Dataset": "Bed Rest",
                    "Subject_ID": br_meta.loc[row, "Subject_ID"],
                    "Phase": br_meta.loc[row, "Analysis_Phase"],
                    "NHANES_Bin": bin_number,
                    "Mahalanobis_Distance": md_from_ref(br_z[row, :], centroid, inv_cov),
                })

    return pd.DataFrame.from_records(records)

def summarize(results: pd.DataFrame) -> pd.DataFrame:
    return (results.groupby(["Dataset", "Phase"], as_index=False)["Mahalanobis_Distance"]
            .agg(N="count", Mean="mean", SD="std", Median="median",
                 Q025=lambda x: x.quantile(0.025), Q25=lambda x: x.quantile(0.25),
                 Q75=lambda x: x.quantile(0.75), Q975=lambda x: x.quantile(0.975), Min="min", Max="max"))


def plot_kde(results: pd.DataFrame, dataset: str, phases: list[str], output_path: Path, title: str):
    plt.figure(figsize=(8, 5))
    for phase in phases:
        vals = results.loc[(results["Dataset"] == dataset) & (results["Phase"] == phase), "Mahalanobis_Distance"].dropna().to_numpy()
        if len(vals) < 2:
            continue
        kde = gaussian_kde(vals)
        xs = np.linspace(vals.min(), vals.max(), 300)
        plt.plot(xs, kde(xs), label=f"{phase} (median={np.median(vals):.2f})")
    plt.xlabel("Mahalanobis distance from bootstrapped NHANES reference")
    plt.ylabel("Density")
    plt.title(title)
    plt.legend(frameon=False)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()


def plot_violin(results: pd.DataFrame, output_path: Path):
    order = [
        ("Inspiration4", "Preflight"),
        ("Inspiration4", "Postflight"),
        ("Bed Rest", "Pre-BR"),
        ("Bed Rest", "In-BR"),
        ("Bed Rest", "Post-BR"),
    ]
    data = [results.loc[(results["Dataset"] == d) & (results["Phase"] == p), "Mahalanobis_Distance"].dropna().to_numpy()
            for d, p in order]
    labels = [f"{d}\n{p}" for d, p in order]

    plt.figure(figsize=(9, 5))
    parts = plt.violinplot(data, showmeans=False, showmedians=True, showextrema=False)
    # Do not force colors; keep Matplotlib defaults.
    for body in parts.get("bodies", []):
        body.set_alpha(0.65)
    x_positions = np.arange(1, len(data) + 1)
    for x, vals in zip(x_positions, data):
        # plot a light jittered sample so the figure remains readable even with many bootstrap results
        if len(vals) > 1000:
            vals_plot = np.random.default_rng(123).choice(vals, size=1000, replace=False)
        else:
            vals_plot = vals
        jitter = np.random.default_rng(123 + x).normal(0, 0.035, size=len(vals_plot))
        plt.scatter(np.full_like(vals_plot, x, dtype=float) + jitter, vals_plot, s=3, alpha=0.08)
    plt.xticks(x_positions, labels)
    plt.ylabel("Mahalanobis distance from bootstrapped NHANES reference")
    plt.title("Overall multivariate deviation from NHANES reference")
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--nhanes", default="nhanes_biopro_all_cycles_combined.csv")
    parser.add_argument("--i4", default="LUNAR_Inspiration4_OVERLAP_Summary_v1.xlsx")
    parser.add_argument("--br", default="LUNAR_BedRest_Campaign1_OVERLAP_Summary_v3.xlsx")
    parser.add_argument("--outdir", default="outputs")
    parser.add_argument("--iterations", type=int, default=1000)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    nhanes = load_nhanes(Path(args.nhanes))
    i4 = load_i4(Path(args.i4))
    br = load_bedrest(Path(args.br))

    nh_z, i4_z, br_z, mu, sd = transform_and_standardize(nhanes, i4, br)

    results = run_bootstrap(nh_z, i4[["Subject_ID", "Analysis_Phase"]].copy(), i4_z,
                            br[["Subject_ID", "Analysis_Phase"]].copy(), br_z,
                            iterations=args.iterations, seed=args.seed)
    summary = summarize(results)

    results.to_csv(outdir / "mahalanobis_long_results.csv", index=False)

    panel = pd.DataFrame({
        "Variable": TRUE_17_VARIABLES,
        "NHANES_Mean_after_transform": [mu[v] for v in TRUE_17_VARIABLES],
        "NHANES_SD_after_transform": [sd[v] for v in TRUE_17_VARIABLES],
        "Log_Transformed": [v in SKEWED_VARS for v in TRUE_17_VARIABLES],
    })
    panel.to_csv(outdir / "analysis_panel_used.csv", index=False)

    with pd.ExcelWriter(outdir / "mahalanobis_distance_summary.xlsx", engine="openpyxl") as writer:
        summary.to_excel(writer, index=False, sheet_name="Summary_By_Phase")
        results.head(50000).to_excel(writer, index=False, sheet_name="Long_Results_First_50000")
        panel.to_excel(writer, index=False, sheet_name="Analysis_Panel")

    plot_kde(results, "Inspiration4", ["Preflight", "Postflight"],
             outdir / "mahalanobis_i4_density.png", "Inspiration4 vs bootstrapped NHANES reference")
    plot_kde(results, "Bed Rest", ["Pre-BR", "In-BR", "Post-BR"],
             outdir / "mahalanobis_br_density.png", "Bed Rest vs bootstrapped NHANES reference")
    plot_violin(results, outdir / "Figure_04_Bootstrap_Mahalanobis_Violin.png")

    print("Done.")
    print(f"NHANES complete-case rows used: {len(nhanes)}")
    print(f"Inspiration4 subject-phase rows used: {len(i4)}")
    print(f"Bed Rest subject-phase rows used: {len(br)}")
    print(f"Outputs written to: {outdir.resolve()}")
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
