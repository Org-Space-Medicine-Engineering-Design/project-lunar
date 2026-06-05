
#!/usr/bin/env python3
"""
LUNAR whole-reference Mahalanobis distance analysis.

This version estimates the NHANES reference centroid and covariance matrix once
from the full complete-case NHANES reference population, then projects each
Inspiration4 and Bed Rest subject-phase profile into that fixed NHANES space.

Inputs expected in the same directory:
  - nhanes_biopro_all_cycles_combined.csv
  - LUNAR_Inspiration4_OVERLAP_Summary_v1.xlsx
  - LUNAR_BedRest_Campaign1_OVERLAP_Summary_v3.xlsx

Outputs:
  - LUNAR_Mahalanobis_Full_NHANES_Reference.xlsx
  - lunar_full_reference_subject_distances.csv
  - lunar_full_reference_phase_summary.csv
  - lunar_full_reference_subject_trajectories.png
  - lunar_full_reference_subject_trajectories.pdf
"""

from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.linalg import pinvh
from scipy.spatial.distance import mahalanobis

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

    out["ALBUMIN/GLOBULIN RATIO"] = out["ALBUMIN"] / out["GLOBULIN"]
    out["BUN/CREATININE RATIO"] = out["BUN"] / out["CREATININE"]

    for var in TRUE_17_VARIABLES:
        out.loc[out[var] <= 0, var] = np.nan

    if "SEQN" in out.columns:
        out = out.groupby("SEQN", as_index=False)[TRUE_17_VARIABLES].first()

    return out.dropna(subset=TRUE_17_VARIABLES).reset_index(drop=True)


def load_i4(path: Path) -> pd.DataFrame:
    df = pd.read_excel(path, sheet_name="Overlap_Data")
    df = df[df["Variable"].isin(TRUE_17_VARIABLES)].copy()
    df["Value"] = pd.to_numeric(df["Value"], errors="coerce")
    df = df.dropna(subset=["Subject_ID", "Timepoint", "Variable", "Value"])

    df["Analysis_Phase"] = np.where(
        df["Timepoint"].isin(I4_PRE_TIMEPOINTS),
        "Preflight",
        np.where(df["Timepoint"].isin(I4_POST_TIMEPOINTS), "Postflight", None),
    )
    df = df.dropna(subset=["Analysis_Phase"])

    avg = df.groupby(["Subject_ID", "Analysis_Phase", "Variable"], as_index=False)["Value"].mean()
    wide = avg.pivot_table(index=["Subject_ID", "Analysis_Phase"], columns="Variable", values="Value", aggfunc="mean")
    wide = wide.reset_index()

    if "ALBUMIN/GLOBULIN RATIO" not in wide.columns:
        wide["ALBUMIN/GLOBULIN RATIO"] = np.nan
    wide["ALBUMIN/GLOBULIN RATIO"] = wide["ALBUMIN/GLOBULIN RATIO"].fillna(wide["ALBUMIN"] / wide["GLOBULIN"])

    if "BUN/CREATININE RATIO" not in wide.columns:
        wide["BUN/CREATININE RATIO"] = np.nan
    wide["BUN/CREATININE RATIO"] = wide["BUN/CREATININE RATIO"].fillna(wide["BUN"] / wide["CREATININE"])

    return wide.dropna(subset=TRUE_17_VARIABLES).reset_index(drop=True)


def load_bedrest(path: Path) -> pd.DataFrame:
    df = pd.read_excel(path, sheet_name="Overlap_Data")
    df["Inspiration4_Variable"] = df["Inspiration4_Variable"].replace({"UREA NITROGEN (BUN)": "BUN"})
    df = df[df["Inspiration4_Variable"].isin(TRUE_17_VARIABLES)].copy()
    df = df[df["Test_Phase"].isin(BR_PHASES)].copy()
    df["Value_Numeric"] = pd.to_numeric(df["Value_Numeric"], errors="coerce")
    df = df.dropna(subset=["Subject_ID", "Test_Phase", "Inspiration4_Variable", "Value_Numeric"])

    avg = df.groupby(["Subject_ID", "Test_Phase", "Inspiration4_Variable"], as_index=False)["Value_Numeric"].mean()
    wide = avg.pivot_table(index=["Subject_ID", "Test_Phase"], columns="Inspiration4_Variable", values="Value_Numeric", aggfunc="mean")
    wide = wide.reset_index().rename(columns={"Test_Phase": "Analysis_Phase"})

    phase_map = {"PRE_TEST": "Pre-BR", "IN_TEST": "In-BR", "POST_TEST": "Post-BR"}
    wide["Analysis_Phase"] = wide["Analysis_Phase"].map(phase_map)

    if "GLOBULIN" not in wide.columns:
        wide["GLOBULIN"] = wide["PROTEIN; TOTAL"] - wide["ALBUMIN"]

    if "ALBUMIN/GLOBULIN RATIO" not in wide.columns:
        wide["ALBUMIN/GLOBULIN RATIO"] = np.nan
    wide["ALBUMIN/GLOBULIN RATIO"] = wide["ALBUMIN/GLOBULIN RATIO"].fillna(wide["ALBUMIN"] / wide["GLOBULIN"])

    if "BUN/CREATININE RATIO" not in wide.columns:
        wide["BUN/CREATININE RATIO"] = np.nan
    wide["BUN/CREATININE RATIO"] = wide["BUN/CREATININE RATIO"].fillna(wide["BUN"] / wide["CREATININE"])

    return wide.dropna(subset=TRUE_17_VARIABLES).reset_index(drop=True)


def transform_data(nhanes: pd.DataFrame, i4: pd.DataFrame, br: pd.DataFrame):
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

    return nh_z, i4_z, br_z, mu, sd


def compute_full_reference_distances(nh_z: pd.DataFrame, i4_z: pd.DataFrame, br_z: pd.DataFrame, i4: pd.DataFrame, br: pd.DataFrame):
    centroid = nh_z.mean(axis=0).to_numpy(float)
    cov = np.cov(nh_z.to_numpy(float), rowvar=False)

    # Small ridge term guards against numerical instability if any biomarkers are nearly collinear.
    cov = cov + np.eye(cov.shape[0]) * 1e-6
    inv_cov = pinvh(cov)

    records = []
    for idx, row in i4.iterrows():
        x = i4_z.loc[idx, TRUE_17_VARIABLES].to_numpy(float)
        records.append({
            "Dataset": "Inspiration4",
            "Subject_ID": row["Subject_ID"],
            "Phase": row["Analysis_Phase"],
            "Mahalanobis_Distance": float(mahalanobis(x, centroid, inv_cov)),
        })

    for idx, row in br.iterrows():
        x = br_z.loc[idx, TRUE_17_VARIABLES].to_numpy(float)
        records.append({
            "Dataset": "Bed Rest",
            "Subject_ID": row["Subject_ID"],
            "Phase": row["Analysis_Phase"],
            "Mahalanobis_Distance": float(mahalanobis(x, centroid, inv_cov)),
        })

    long = pd.DataFrame.from_records(records)

    phase_order = ["Preflight", "Postflight", "Pre-BR", "In-BR", "Post-BR"]
    phase_summary = (
        long.groupby(["Dataset", "Phase"], as_index=False)
        .agg(
            N=("Mahalanobis_Distance", "count"),
            Mean=("Mahalanobis_Distance", "mean"),
            SD=("Mahalanobis_Distance", "std"),
            Median=("Mahalanobis_Distance", "median"),
            Min=("Mahalanobis_Distance", "min"),
            Max=("Mahalanobis_Distance", "max"),
        )
    )
    phase_summary["Phase_Order"] = phase_summary["Phase"].map({p: i for i, p in enumerate(phase_order)})
    phase_summary = phase_summary.sort_values(["Dataset", "Phase_Order"]).drop(columns="Phase_Order")

    return long, phase_summary, centroid, cov, inv_cov


def plot_trajectories(long: pd.DataFrame, out_png: Path, out_pdf: Path):
    phase_x = {
        "Preflight": 0,
        "Postflight": 1,
        "Pre-BR": 3,
        "In-BR": 4,
        "Post-BR": 5,
    }
    x_labels = {
        0: "I4\nPreflight",
        1: "I4\nPostflight",
        3: "BR\nPre-BR",
        4: "BR\nIn-BR",
        5: "BR\nPost-BR",
    }

    i4_subjects = sorted(long.loc[long["Dataset"] == "Inspiration4", "Subject_ID"].unique())
    br_subjects = sorted(long.loc[long["Dataset"] == "Bed Rest", "Subject_ID"].unique())

    colors = {
        i4_subjects[0]: "#D62728",
        i4_subjects[1]: "#1F77B4",
        i4_subjects[2]: "#2CA02C",
        i4_subjects[3]: "#9467BD",
        br_subjects[0]: "#FF7F0E",
        br_subjects[1]: "#17BECF",
        br_subjects[2]: "#E377C2",
    }

    labels = {
        i4_subjects[0]: f"Crew member 1 ({i4_subjects[0]})",
        i4_subjects[1]: f"Crew member 2 ({i4_subjects[1]})",
        i4_subjects[2]: f"Crew member 3 ({i4_subjects[2]})",
        i4_subjects[3]: f"Crew member 4 ({i4_subjects[3]})",
        br_subjects[0]: f"Bed rest subject 1 ({br_subjects[0]})",
        br_subjects[1]: f"Bed rest subject 2 ({br_subjects[1]})",
        br_subjects[2]: f"Bed rest subject 3 ({br_subjects[2]})",
    }

    plt.rcParams.update({
        "font.family": "DejaVu Sans",
        "font.size": 11,
        "axes.titlesize": 18,
        "axes.labelsize": 13,
        "legend.fontsize": 9,
    })

    fig, ax = plt.subplots(figsize=(11.5, 7))

    for subject in i4_subjects + br_subjects:
        sub = long[long["Subject_ID"] == subject].copy()
        sub["x"] = sub["Phase"].map(phase_x)
        sub = sub.sort_values("x")
        ax.plot(
            sub["x"],
            sub["Mahalanobis_Distance"],
            marker="o",
            markersize=7,
            linewidth=2.2,
            color=colors[subject],
            label=labels[subject],
        )

    ax.set_xlim(-0.35, 5.35)
    ax.set_ylim(bottom=0)
    ax.set_xticks(list(x_labels.keys()))
    ax.set_xticklabels([x_labels[x] for x in x_labels])
    ax.set_ylabel("Mahalanobis distance from NHANES reference")
    ax.set_title("Whole-reference Mahalanobis distance by subject and phase")
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    ax.grid(axis="x", linestyle="-", alpha=0.08)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    ax.text(
        0.5, -0.16,
        "Smaller distance = more similar to the full NHANES reference profile; larger distance = greater multivariate deviation.",
        transform=ax.transAxes,
        ha="center",
        va="top",
        fontsize=10,
        style="italic",
    )

    ax.legend(title="Subject", loc="center left", bbox_to_anchor=(1.01, 0.5), frameon=True)
    fig.tight_layout(rect=[0, 0.05, 0.80, 1])
    fig.savefig(out_png, dpi=300, bbox_inches="tight")
    fig.savefig(out_pdf, bbox_inches="tight")
    plt.close(fig)


def build_workbook(output_path: Path, long: pd.DataFrame, phase_summary: pd.DataFrame, delta_table: pd.DataFrame, reference_stats: pd.DataFrame, analysis_panel: pd.DataFrame, method_rows: list[list]):
    from artifact_tool import Workbook, SpreadsheetFile

    wb = Workbook.create()

    header_format = {
        "fill": "#1F4E79",
        "font": {"bold": True, "color": "#FFFFFF"},
        "horizontal_alignment": "center",
        "vertical_alignment": "center",
    }
    title_format = {
        "fill": "#D9EAF7",
        "font": {"bold": True, "size": 14, "color": "#17365D"},
        "horizontal_alignment": "left",
    }

    def write_df(sheet_name: str, df_in: pd.DataFrame, table_name: str):
        ws = wb.worksheets.add(sheet_name)
        clean_df = df_in.astype(object).where(pd.notnull(df_in), None)
        values = [clean_df.columns.tolist()] + clean_df.values.tolist()
        end_col_idx = len(values[0]) - 1
        end_row = len(values)
        # convert col idx to Excel letters
        def col_letter(n):
            s = ""
            n += 1
            while n:
                n, r = divmod(n - 1, 26)
                s = chr(65 + r) + s
            return s
        end_col = col_letter(end_col_idx)
        rng_addr = f"A1:{end_col}{end_row}"
        ws.get_range(rng_addr).values = values
        ws.get_range(f"A1:{end_col}1").format = header_format
        ws.tables.add(rng_addr, True, table_name)
        ws.freeze_panes.freeze_rows(1)
        ws.get_range(rng_addr).format.autofit_columns()
        return ws

    # README / Methods
    ws = wb.worksheets.add("README_Methods")
    ws.get_range("A1:E1").merge()
    ws.get_range("A1").values = [["LUNAR Whole-Reference Mahalanobis Distance Analysis"]]
    ws.get_range("A1").format = title_format
    ws.get_range("A3:B" + str(2 + len(method_rows))).values = method_rows
    ws.get_range("A3:B3").format = header_format
    ws.get_range("A:B").format.wrap_text = True
    ws.get_range("A:A").format.column_width = 28
    ws.get_range("B:B").format.column_width = 95
    ws.freeze_panes.freeze_rows(3)

    write_df("Subject_Distances", long, "SubjectDistancesTable")
    write_df("Phase_Summary", phase_summary, "PhaseSummaryTable")
    write_df("Phase_Deltas", delta_table, "PhaseDeltasTable")
    write_df("NHANES_Reference", reference_stats, "NHANESReferenceTable")
    write_df("Analysis_Panel", analysis_panel, "AnalysisPanelTable")

    # Number formats
    for sheet_name in ["Subject_Distances", "Phase_Summary", "Phase_Deltas", "NHANES_Reference", "Analysis_Panel"]:
        ws = wb.worksheets.get_item(sheet_name)
        # Apply broad number formatting to likely numeric columns
        ws.get_range("A:Z").format.autofit_columns()

    SpreadsheetFile.export_xlsx(wb).save(str(output_path))


def main():
    base = Path(".")
    nhanes_path = base / "nhanes_biopro_all_cycles_combined.csv"
    i4_path = base / "LUNAR_Inspiration4_OVERLAP_Summary_v1.xlsx"
    br_path = base / "LUNAR_BedRest_Campaign1_OVERLAP_Summary_v3.xlsx"

    nhanes = load_nhanes(nhanes_path)
    i4 = load_i4(i4_path)
    br = load_bedrest(br_path)

    nh_z, i4_z, br_z, mu, sd = transform_data(nhanes, i4, br)
    long, phase_summary, centroid, cov, inv_cov = compute_full_reference_distances(nh_z, i4_z, br_z, i4, br)

    # Add phase ordering and sort for readability
    phase_order = {"Preflight": 1, "Postflight": 2, "Pre-BR": 3, "In-BR": 4, "Post-BR": 5}
    long["Phase_Order"] = long["Phase"].map(phase_order)
    long = long.sort_values(["Dataset", "Subject_ID", "Phase_Order"]).drop(columns="Phase_Order").reset_index(drop=True)

    phase_summary["Phase_Order"] = phase_summary["Phase"].map(phase_order)
    phase_summary = phase_summary.sort_values(["Dataset", "Phase_Order"]).drop(columns="Phase_Order").reset_index(drop=True)

    # Deltas
    i4_delta = long[long["Dataset"] == "Inspiration4"].pivot(index="Subject_ID", columns="Phase", values="Mahalanobis_Distance").reset_index()
    if {"Preflight", "Postflight"}.issubset(i4_delta.columns):
        i4_delta["Post_minus_Pre"] = i4_delta["Postflight"] - i4_delta["Preflight"]
        i4_delta = i4_delta.rename(columns={"Preflight": "Preflight_Distance", "Postflight": "Postflight_Distance"})
        i4_delta["Dataset"] = "Inspiration4"
        i4_delta = i4_delta[["Dataset", "Subject_ID", "Preflight_Distance", "Postflight_Distance", "Post_minus_Pre"]]
    else:
        i4_delta = pd.DataFrame()

    br_delta = long[long["Dataset"] == "Bed Rest"].pivot(index="Subject_ID", columns="Phase", values="Mahalanobis_Distance").reset_index()
    if {"Pre-BR", "In-BR", "Post-BR"}.issubset(br_delta.columns):
        br_delta["In_minus_Pre"] = br_delta["In-BR"] - br_delta["Pre-BR"]
        br_delta["Post_minus_Pre"] = br_delta["Post-BR"] - br_delta["Pre-BR"]
        br_delta["Post_minus_In"] = br_delta["Post-BR"] - br_delta["In-BR"]
        br_delta = br_delta.rename(columns={"Pre-BR": "Pre_BR_Distance", "In-BR": "In_BR_Distance", "Post-BR": "Post_BR_Distance"})
        br_delta["Dataset"] = "Bed Rest"
        br_delta = br_delta[["Dataset", "Subject_ID", "Pre_BR_Distance", "In_BR_Distance", "Post_BR_Distance", "In_minus_Pre", "Post_minus_Pre", "Post_minus_In"]]
    else:
        br_delta = pd.DataFrame()

    delta_table = pd.concat([i4_delta, br_delta], ignore_index=True, sort=False)
    if not delta_table.empty:
        long = long.merge(delta_table[["Dataset", "Subject_ID"]], on=["Dataset", "Subject_ID"], how="left")

    # Reference stats
    reference_stats = pd.DataFrame({
        "Variable": TRUE_17_VARIABLES,
        "NHANES_Mean_after_transform": mu.values,
        "NHANES_SD_after_transform": sd.values,
        "NHANES_Z_Centroid": centroid,
        "Log_Transformed": [v in SKEWED_VARS for v in TRUE_17_VARIABLES],
    })
    reference_stats.insert(0, "NHANES_Complete_Case_N", len(nhanes))

    analysis_panel = pd.DataFrame({
        "Variable": TRUE_17_VARIABLES,
        "NHANES_Column_Primary": [NHANES_MAP.get(v, "") for v in TRUE_17_VARIABLES],
        "NHANES_Column_Secondary": [NHANES_SECOND_DAY_MAP.get(v, "") for v in TRUE_17_VARIABLES],
        "Derived_in_NHANES": [v in ["ALBUMIN/GLOBULIN RATIO", "BUN/CREATININE RATIO"] for v in TRUE_17_VARIABLES],
        "Log_Transformed": [v in SKEWED_VARS for v in TRUE_17_VARIABLES],
    })

    method_rows = [
        ["Section", "Description"],
        ["Reference population", f"NHANES complete-case participants with non-missing positive values for all 17 biomarkers were retained (N = {len(nhanes):,})."],
        ["Biomarker panel", "The 17-variable panel excluded CRP because CRP was not available in NHANES."],
        ["Phase aggregation", "Inspiration4 preflight was averaged across L-92, L-44, and L-3; postflight was averaged across R+1, R+45, R+82, and R+194. Bed rest was summarized as Pre-BR, In-BR, and Post-BR."],
        ["Transformation", "Right-skewed markers were natural-log transformed before reference scaling."],
        ["Standardization", "All variables were centered and scaled using means and standard deviations estimated from the full NHANES reference population."],
        ["Mahalanobis reference", "The NHANES centroid and covariance matrix were estimated once from the full NHANES reference population. No pseudo-crew binning or bootstrap resampling was used."],
        ["Distance interpretation", "Smaller Mahalanobis distance indicates greater similarity to the NHANES reference profile; larger distance indicates greater multivariate deviation from the NHANES reference profile."],
    ]

    # Write CSV outputs
    long.to_csv("lunar_full_reference_subject_distances.csv", index=False)
    phase_summary.to_csv("lunar_full_reference_phase_summary.csv", index=False)
    delta_table.to_csv("lunar_full_reference_phase_deltas.csv", index=False)
    reference_stats.to_csv("lunar_full_reference_nhanes_stats.csv", index=False)

    plot_trajectories(
        long,
        Path("lunar_full_reference_subject_trajectories.png"),
        Path("lunar_full_reference_subject_trajectories.pdf")
    )

    # Build workbook
    # Include deltas by merging as an additional sheet if using artifact_tool manually.
    build_workbook(
        Path("LUNAR_Mahalanobis_Full_NHANES_Reference.xlsx"),
        long,
        phase_summary,
        delta_table,
        reference_stats,
        analysis_panel,
        method_rows,
    )

    print("Complete.")
    print(f"NHANES complete-case N: {len(nhanes):,}")
    print("Subject distances:")
    print(long.to_string(index=False))
    print("Phase summary:")
    print(phase_summary.to_string(index=False))


if __name__ == "__main__":
    main()
