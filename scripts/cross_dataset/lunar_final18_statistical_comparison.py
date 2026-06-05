#!/usr/bin/env python3
"""
LUNAR Final 18 Statistical Comparison Pipeline

This script generates an Excel statistical comparison workbook for the LUNAR project
using individual-level data from:

1. NHANES biochemical profile data
2. Inspiration4 individual-level wide-format data
3. UTMB Bed Rest Campaign 1 individual-level long-format data
4. NHANES overlap/crosswalk workbook

Primary analyses:
- Restrict to final 18 overlapping biochemical measures
- Calculate NHANES reference mean and SD
- Convert Inspiration4 and Bed Rest observations to NHANES-referenced z-scores
- Compare cohort z-scores against NHANES reference mean of z = 0
- Compare Bed Rest and Inspiration4 cohorts
- Perform repeated-measures ANOVA over time within Inspiration4 and Bed Rest
- Include raw and log10-transformed CRP repeated-measures ANOVA
- Apply Benjamini-Hochberg FDR correction

Author: LUNAR Project
"""

import argparse
import math
import os
import re
import warnings

import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.stats.anova import AnovaRM
from statsmodels.stats.multitest import multipletests

warnings.filterwarnings("ignore")


FINAL_18_VARIABLES = [
    "ALBUMIN",
    "ALBUMIN/GLOBULIN RATIO",
    "ALKALINE PHOSPHATASE",
    "ALT",
    "AST",
    "BILIRUBIN; TOTAL",
    "BUN",
    "BUN/CREATININE RATIO",
    "CALCIUM",
    "CARBON DIOXIDE",
    "CHLORIDE",
    "CREATININE",
    "CRP",
    "GLOBULIN",
    "GLUCOSE",
    "POTASSIUM",
    "PROTEIN; TOTAL",
    "SODIUM",
]


I4_COLUMN_MAP = {
    "ALBUMIN": "CMP__ALBUMIN",
    "ALBUMIN/GLOBULIN RATIO": "CMP__ALBUMIN/GLOBULIN RATIO",
    "ALKALINE PHOSPHATASE": "CMP__ALKALINE PHOSPHATASE",
    "ALT": "CMP__ALT",
    "AST": "CMP__AST",
    "BILIRUBIN; TOTAL": "CMP__BILIRUBIN; TOTAL",
    "BUN": "CMP__UREA NITROGEN (BUN)",
    "BUN/CREATININE RATIO": "CMP__BUN/CREATININE RATIO",
    "CALCIUM": "CMP__CALCIUM",
    "CARBON DIOXIDE": "CMP__CARBON DIOXIDE",
    "CHLORIDE": "CMP__CHLORIDE",
    "CREATININE": "CMP__CREATININE",
    "CRP": "Inflammation__CRP",
    "GLOBULIN": "CMP__GLOBULIN",
    "GLUCOSE": "CMP__GLUCOSE",
    "POTASSIUM": "CMP__POTASSIUM",
    "PROTEIN; TOTAL": "CMP__PROTEIN; TOTAL",
    "SODIUM": "CMP__SODIUM",
}


BR_VARIABLE_MAP = {
    "ALBUMIN": "ALBUMIN",
    "ALBUMIN/GLOBULIN RATIO": "ALBUMIN/GLOBULIN RATIO",
    "ALKALINE PHOSPHATASE": "ALKALINE PHOSPHATASE",
    "ALT": "ALT",
    "AST": "AST",
    "BILIRUBIN; TOTAL": "BILIRUBIN; TOTAL",
    "BUN": "UREA NITROGEN (BUN)",
    "BUN/CREATININE RATIO": "BUN/CREATININE RATIO",
    "CALCIUM": "CALCIUM",
    "CARBON DIOXIDE": "CARBON DIOXIDE",
    "CHLORIDE": "CHLORIDE",
    "CREATININE": "CREATININE",
    "CRP": "CRP",
    "GLOBULIN": "GLOBULIN",
    "GLUCOSE": "GLUCOSE",
    "POTASSIUM": "POTASSIUM",
    "PROTEIN; TOTAL": "PROTEIN; TOTAL",
    "SODIUM": "SODIUM",
}


def safe_numeric(series):
    """Convert a pandas Series to numeric values, coercing invalid entries to NaN."""
    return pd.to_numeric(series, errors="coerce")


def normalize_name(value):
    """Normalize variable names for robust matching."""
    return re.sub(r"[^A-Z0-9]+", "", str(value).upper())


def mean_ci_95(values):
    """Return the two-sided 95% confidence interval for a numeric vector."""
    values = pd.Series(values).dropna()
    n = len(values)

    if n < 2:
        return np.nan, np.nan

    mean_value = values.mean()
    se = values.std(ddof=1) / math.sqrt(n)
    tcrit = stats.t.ppf(0.975, n - 1)

    return mean_value - tcrit * se, mean_value + tcrit * se


def apply_bh_fdr(df, p_col="p_value", out_col="FDR_BH"):
    """Apply Benjamini-Hochberg FDR correction to a p-value column."""
    df = df.copy()
    df[out_col] = np.nan

    if p_col not in df.columns:
        return df

    valid = df[p_col].notna()
    if valid.sum() > 0:
        df.loc[valid, out_col] = multipletests(df.loc[valid, p_col], method="fdr_bh")[1]

    return df


def cohen_d_independent(x, y):
    """Compute Cohen's d for two independent samples."""
    x = pd.Series(x).dropna()
    y = pd.Series(y).dropna()

    if len(x) < 2 or len(y) < 2:
        return np.nan

    sx = x.std(ddof=1)
    sy = y.std(ddof=1)
    pooled_n = len(x) + len(y) - 2

    if pooled_n <= 0:
        return np.nan

    pooled_sd = math.sqrt(((len(x) - 1) * sx**2 + (len(y) - 1) * sy**2) / pooled_n)

    if pooled_sd == 0:
        return np.nan

    return (x.mean() - y.mean()) / pooled_sd


def hedges_g_from_d(d, nx, ny):
    """Convert Cohen's d to Hedges' g using small-sample correction."""
    if pd.isna(d) or nx + ny <= 3:
        return np.nan

    correction = 1 - (3 / (4 * (nx + ny) - 9))
    return d * correction


def cohen_dz_paired(differences):
    """Compute Cohen's dz for paired data."""
    differences = pd.Series(differences).dropna()

    if len(differences) < 2:
        return np.nan

    sd = differences.std(ddof=1)

    if sd == 0:
        return np.nan

    return differences.mean() / sd


def read_nhanes_overlap_map(overlap_workbook):
    """
    Read NHANES overlap mapping from the overlap workbook.

    Expected sheet:
    - Variable_Stats

    Expected columns:
    - Canonical_Name
    - Variable
    """
    stats_df = pd.read_excel(overlap_workbook, sheet_name="Variable_Stats")

    required = {"Canonical_Name", "Variable"}
    missing = required - set(stats_df.columns)

    if missing:
        raise ValueError(
            f"NHANES overlap workbook is missing required columns: {sorted(missing)}"
        )

    mapping = dict(zip(stats_df["Canonical_Name"], stats_df["Variable"]))

    # Harmonize display names used in this final 18 analysis.
    harmonized = {}
    for key, value in mapping.items():
        k = str(key).upper().strip()

        if k in {"UREA NITROGEN (BUN)", "BUN"}:
            harmonized["BUN"] = value
        elif k in {"ALBUMIN_GLOBULIN RATIO", "ALBUMIN/GLOBULIN RATIO"}:
            harmonized["ALBUMIN/GLOBULIN RATIO"] = value
        elif k in {"BUN_CREATININE RATIO", "BUN/CREATININE RATIO"}:
            harmonized["BUN/CREATININE RATIO"] = value
        else:
            harmonized[k] = value

    return harmonized


def add_derived_nhanes_variables(nhanes):
    """Add derived ratio variables to NHANES when component columns are available."""
    nhanes = nhanes.copy()

    if "ALBUMIN_GLOBULIN_RATIO" not in nhanes.columns:
        if {"LBXSAL", "LBXSGB"}.issubset(nhanes.columns):
            nhanes["ALBUMIN_GLOBULIN_RATIO"] = (
                safe_numeric(nhanes["LBXSAL"]) / safe_numeric(nhanes["LBXSGB"])
            )

    if "BUN_CREATININE_RATIO" not in nhanes.columns:
        if {"LBXSBU", "LBXSCR"}.issubset(nhanes.columns):
            nhanes["BUN_CREATININE_RATIO"] = (
                safe_numeric(nhanes["LBXSBU"]) / safe_numeric(nhanes["LBXSCR"])
            )

    return nhanes


def prepare_bedrest_wide(bedrest):
    """
    Convert Bed Rest long-format data to subject-phase wide format.

    Expected columns:
    - Subject_ID
    - Test_Phase
    - Variable_Canonical
    - Value_Numeric
    """
    required = {"Subject_ID", "Test_Phase", "Variable_Canonical", "Value_Numeric"}
    missing = required - set(bedrest.columns)

    if missing:
        raise ValueError(f"Bed Rest file is missing required columns: {sorted(missing)}")

    bedrest = bedrest.copy()
    bedrest["Phase_Group"] = bedrest["Test_Phase"].map(
        {
            "PRE_TEST": "BR_Pre",
            "IN_TEST": "BR_In",
            "POST_TEST": "BR_Post",
        }
    )
    bedrest["Value_Numeric"] = safe_numeric(bedrest["Value_Numeric"])

    bedrest = bedrest.dropna(
        subset=["Subject_ID", "Phase_Group", "Variable_Canonical", "Value_Numeric"]
    )

    bedrest_agg = (
        bedrest.groupby(["Subject_ID", "Phase_Group", "Variable_Canonical"], as_index=False)[
            "Value_Numeric"
        ]
        .mean()
    )

    bedrest_wide = bedrest_agg.pivot_table(
        index=["Subject_ID", "Phase_Group"],
        columns="Variable_Canonical",
        values="Value_Numeric",
        aggfunc="mean",
    ).reset_index()

    # Derived Bed Rest variables if not already present.
    if "GLOBULIN" not in bedrest_wide.columns:
        if {"PROTEIN; TOTAL", "ALBUMIN"}.issubset(bedrest_wide.columns):
            bedrest_wide["GLOBULIN"] = (
                bedrest_wide["PROTEIN; TOTAL"] - bedrest_wide["ALBUMIN"]
            )

    if "ALBUMIN/GLOBULIN RATIO" not in bedrest_wide.columns:
        if {"ALBUMIN", "GLOBULIN"}.issubset(bedrest_wide.columns):
            bedrest_wide["ALBUMIN/GLOBULIN RATIO"] = (
                bedrest_wide["ALBUMIN"] / bedrest_wide["GLOBULIN"].replace(0, np.nan)
            )

    if "BUN/CREATININE RATIO" not in bedrest_wide.columns:
        if {"UREA NITROGEN (BUN)", "CREATININE"}.issubset(bedrest_wide.columns):
            bedrest_wide["BUN/CREATININE RATIO"] = (
                bedrest_wide["UREA NITROGEN (BUN)"]
                / bedrest_wide["CREATININE"].replace(0, np.nan)
            )

    return bedrest_wide


def make_nhanes_reference(nhanes, nhanes_map):
    """Calculate NHANES reference statistics for the final 18 variables."""
    rows = []

    for variable in FINAL_18_VARIABLES:
        nh_col = nhanes_map.get(variable)

        if nh_col is None or nh_col not in nhanes.columns:
            rows.append(
                {
                    "Variable": variable,
                    "NHANES_Column": nh_col,
                    "NHANES_Available": False,
                    "NHANES_N": 0,
                    "NHANES_Mean": np.nan,
                    "NHANES_SD": np.nan,
                    "NHANES_Median": np.nan,
                    "NHANES_Min": np.nan,
                    "NHANES_Max": np.nan,
                }
            )
            continue

        values = safe_numeric(nhanes[nh_col]).dropna()

        rows.append(
            {
                "Variable": variable,
                "NHANES_Column": nh_col,
                "NHANES_Available": len(values) > 0,
                "NHANES_N": len(values),
                "NHANES_Mean": values.mean() if len(values) else np.nan,
                "NHANES_SD": values.std(ddof=1) if len(values) > 1 else np.nan,
                "NHANES_Median": values.median() if len(values) else np.nan,
                "NHANES_Min": values.min() if len(values) else np.nan,
                "NHANES_Max": values.max() if len(values) else np.nan,
            }
        )

    return pd.DataFrame(rows)


def build_mapping_status(nhanes_reference, inspiration4, bedrest_wide):
    """Create variable mapping and availability status table."""
    rows = []

    for variable in FINAL_18_VARIABLES:
        i4_col = I4_COLUMN_MAP.get(variable)
        br_col = BR_VARIABLE_MAP.get(variable)

        i4_available = (
            i4_col is not None
            and i4_col in inspiration4.columns
            and safe_numeric(inspiration4[i4_col]).notna().sum() > 0
        )

        br_available = (
            br_col is not None
            and br_col in bedrest_wide.columns
            and safe_numeric(bedrest_wide[br_col]).notna().sum() > 0
        )

        ref_row = nhanes_reference.loc[nhanes_reference["Variable"].eq(variable)]
        nh_col = ref_row["NHANES_Column"].iloc[0] if len(ref_row) else np.nan
        nh_available = bool(ref_row["NHANES_Available"].iloc[0]) if len(ref_row) else False

        rows.append(
            {
                "Variable": variable,
                "NHANES_Column": nh_col,
                "NHANES_Available": nh_available,
                "I4_Column": i4_col,
                "I4_Available": i4_available,
                "BR_Source_or_Derived_Column": br_col,
                "BR_Available": br_available,
            }
        )

    return pd.DataFrame(rows)


def build_individual_zscores(inspiration4, bedrest_wide, nhanes_reference):
    """Build individual NHANES-normalized z-score table for I4 and Bed Rest."""
    records = []

    i4_group_map = {}
    for timepoint in inspiration4["Timepoint"].dropna().unique():
        timepoint_str = str(timepoint)

        if timepoint_str.startswith("L-"):
            i4_group_map[timepoint] = "I4_Pre"
        elif timepoint_str.startswith("R+"):
            i4_group_map[timepoint] = "I4_Post"

    for _, ref_row in nhanes_reference.iterrows():
        variable = ref_row["Variable"]
        mean = ref_row["NHANES_Mean"]
        sd = ref_row["NHANES_SD"]

        if not np.isfinite(mean) or not np.isfinite(sd) or sd == 0:
            continue

        # Inspiration4
        i4_col = I4_COLUMN_MAP.get(variable)
        if i4_col is not None and i4_col in inspiration4.columns:
            for _, row in inspiration4.iterrows():
                group = i4_group_map.get(row.get("Timepoint"))

                if group is None:
                    continue

                value = pd.to_numeric(row.get(i4_col), errors="coerce")

                if pd.notna(value):
                    z = (value - mean) / sd

                    records.append(
                        {
                            "Dataset": "Inspiration4",
                            "Cohort_Group": group,
                            "Subject_ID": row.get("Subject_ID"),
                            "Timepoint": row.get("Timepoint"),
                            "Variable": variable,
                            "Raw_Value": value,
                            "NHANES_Mean": mean,
                            "NHANES_SD": sd,
                            "Z_Score": z,
                            "NHANES_Percentile": stats.norm.cdf(z) * 100,
                        }
                    )

        # Bed Rest
        br_col = BR_VARIABLE_MAP.get(variable)
        if br_col is not None and br_col in bedrest_wide.columns:
            for _, row in bedrest_wide.iterrows():
                value = pd.to_numeric(row.get(br_col), errors="coerce")

                if pd.notna(value):
                    z = (value - mean) / sd

                    records.append(
                        {
                            "Dataset": "Bed Rest",
                            "Cohort_Group": row.get("Phase_Group"),
                            "Subject_ID": row.get("Subject_ID"),
                            "Timepoint": row.get("Phase_Group"),
                            "Variable": variable,
                            "Raw_Value": value,
                            "NHANES_Mean": mean,
                            "NHANES_SD": sd,
                            "Z_Score": z,
                            "NHANES_Percentile": stats.norm.cdf(z) * 100,
                        }
                    )

    return pd.DataFrame(records)


def summarize_groups(zscores):
    """Summarize z-scores by variable and cohort group with one-sample tests vs NHANES."""
    rows = []

    groups = ["BR_Pre", "BR_In", "BR_Post", "I4_Pre", "I4_Post"]

    for variable in FINAL_18_VARIABLES:
        for group in groups:
            subset = zscores[
                zscores["Variable"].eq(variable) & zscores["Cohort_Group"].eq(group)
            ]
            z = subset["Z_Score"].dropna()
            n = len(z)
            ci_low, ci_high = mean_ci_95(z)

            if n >= 2 and z.std(ddof=1) > 0:
                t_stat, p_value = stats.ttest_1samp(z, popmean=0)
            else:
                t_stat, p_value = np.nan, np.nan

            rows.append(
                {
                    "Variable": variable,
                    "Cohort_Group": group,
                    "N": n,
                    "Mean_Z": z.mean() if n else np.nan,
                    "SD_Z": z.std(ddof=1) if n > 1 else np.nan,
                    "Median_Z": z.median() if n else np.nan,
                    "CI95_Low": ci_low,
                    "CI95_High": ci_high,
                    "NHANES_Percentile_of_Mean_Z": (
                        stats.norm.cdf(z.mean()) * 100 if n else np.nan
                    ),
                    "OneSample_t_vs_NHANES_0": t_stat,
                    "p_value_vs_NHANES_0": p_value,
                    "Mean_Raw_Value": subset["Raw_Value"].mean() if n else np.nan,
                    "SD_Raw_Value": subset["Raw_Value"].std(ddof=1) if n > 1 else np.nan,
                    "Status": "OK" if n else "No NHANES-referenced data available",
                }
            )

    summary = pd.DataFrame(rows)
    summary = apply_bh_fdr(
        summary, p_col="p_value_vs_NHANES_0", out_col="FDR_BH_vs_NHANES_0"
    )

    return summary


def pairwise_tests(zscores):
    """Run pairwise z-score comparisons across major cohort groupings."""
    pair_specs = [
        ("BR_Pre", "I4_Pre"),
        ("BR_Post", "I4_Post"),
        ("BR_In", "I4_Post"),
        ("BR_Pre", "BR_In"),
        ("BR_In", "BR_Post"),
        ("BR_Pre", "BR_Post"),
        ("I4_Pre", "I4_Post"),
    ]

    rows = []

    for variable in FINAL_18_VARIABLES:
        var_df = zscores[zscores["Variable"].eq(variable)]

        for group_1, group_2 in pair_specs:
            d1 = var_df[var_df["Cohort_Group"].eq(group_1)]
            d2 = var_df[var_df["Cohort_Group"].eq(group_2)]

            if d1.empty or d2.empty:
                rows.append(
                    {
                        "Variable": variable,
                        "Comparison": f"{group_1} vs {group_2}",
                        "Group_1": group_1,
                        "Group_2": group_2,
                        "Test": "Not performed",
                        "N_Group_1": len(d1),
                        "N_Group_2": len(d2),
                        "N_Paired": np.nan,
                        "Mean_Z_Group_1": d1["Z_Score"].mean() if len(d1) else np.nan,
                        "Mean_Z_Group_2": d2["Z_Score"].mean() if len(d2) else np.nan,
                        "Difference_Group1_minus_Group2": np.nan,
                        "Statistic": np.nan,
                        "p_value": np.nan,
                        "Effect_Size": np.nan,
                        "Effect_Size_Type": "",
                        "Status": "Missing data in one or both groups",
                    }
                )
                continue

            same_dataset = d1["Dataset"].iloc[0] == d2["Dataset"].iloc[0]

            if same_dataset:
                p1 = (
                    d1.groupby("Subject_ID", as_index=False)["Z_Score"]
                    .mean()
                    .rename(columns={"Z_Score": "Z1"})
                )
                p2 = (
                    d2.groupby("Subject_ID", as_index=False)["Z_Score"]
                    .mean()
                    .rename(columns={"Z_Score": "Z2"})
                )
                paired = p1.merge(p2, on="Subject_ID", how="inner")

                if len(paired) >= 2:
                    diff = paired["Z1"] - paired["Z2"]

                    if diff.std(ddof=1) > 0:
                        stat, p_value = stats.ttest_rel(paired["Z1"], paired["Z2"])
                        effect_size = cohen_dz_paired(diff)
                        status = "OK"
                    else:
                        stat, p_value, effect_size = np.nan, np.nan, np.nan
                        status = "Zero variance in paired differences"
                else:
                    diff = pd.Series(dtype=float)
                    stat, p_value, effect_size = np.nan, np.nan, np.nan
                    status = "Insufficient paired observations"

                rows.append(
                    {
                        "Variable": variable,
                        "Comparison": f"{group_1} vs {group_2}",
                        "Group_1": group_1,
                        "Group_2": group_2,
                        "Test": "Paired t-test on subject mean z-scores",
                        "N_Group_1": len(p1),
                        "N_Group_2": len(p2),
                        "N_Paired": len(paired),
                        "Mean_Z_Group_1": paired["Z1"].mean() if len(paired) else np.nan,
                        "Mean_Z_Group_2": paired["Z2"].mean() if len(paired) else np.nan,
                        "Difference_Group1_minus_Group2": (
                            diff.mean() if len(diff) else np.nan
                        ),
                        "Statistic": stat,
                        "p_value": p_value,
                        "Effect_Size": effect_size,
                        "Effect_Size_Type": "Cohen dz",
                        "Status": status,
                    }
                )

            else:
                z1 = d1["Z_Score"].dropna()
                z2 = d2["Z_Score"].dropna()

                if len(z1) >= 2 and len(z2) >= 2:
                    stat, p_value = stats.ttest_ind(z1, z2, equal_var=False)
                    d = cohen_d_independent(z1, z2)
                    effect_size = hedges_g_from_d(d, len(z1), len(z2))
                    status = "OK"
                else:
                    stat, p_value, effect_size = np.nan, np.nan, np.nan
                    status = "Insufficient independent observations"

                rows.append(
                    {
                        "Variable": variable,
                        "Comparison": f"{group_1} vs {group_2}",
                        "Group_1": group_1,
                        "Group_2": group_2,
                        "Test": "Welch t-test on individual z-scores",
                        "N_Group_1": len(z1),
                        "N_Group_2": len(z2),
                        "N_Paired": np.nan,
                        "Mean_Z_Group_1": z1.mean() if len(z1) else np.nan,
                        "Mean_Z_Group_2": z2.mean() if len(z2) else np.nan,
                        "Difference_Group1_minus_Group2": (
                            z1.mean() - z2.mean() if len(z1) and len(z2) else np.nan
                        ),
                        "Statistic": stat,
                        "p_value": p_value,
                        "Effect_Size": effect_size,
                        "Effect_Size_Type": "Hedges g",
                        "Status": status,
                    }
                )

    pairwise = pd.DataFrame(rows)
    pairwise = apply_bh_fdr(pairwise, p_col="p_value", out_col="FDR_BH")

    return pairwise


def run_rm_anova_complete_cases(
    df,
    subject_col,
    time_col,
    value_col,
    dataset_name,
    variable,
    time_order=None,
):
    """
    Run repeated-measures ANOVA using complete cases only.

    Returns a dictionary with F statistic, degrees of freedom, p-value,
    and partial eta squared.
    """
    tmp = df[[subject_col, time_col, value_col]].copy()
    tmp[value_col] = safe_numeric(tmp[value_col])
    tmp = tmp.dropna(subset=[subject_col, time_col, value_col])

    if tmp.empty:
        return {
            "Dataset": dataset_name,
            "Variable": variable,
            "N_Subjects_Complete": 0,
            "N_Timepoints": 0,
            "Timepoints": "",
            "F": np.nan,
            "Num_DF": np.nan,
            "Den_DF": np.nan,
            "p_value": np.nan,
            "Partial_Eta_Squared": np.nan,
            "Status": "No data",
        }

    tmp = tmp.groupby([subject_col, time_col], as_index=False)[value_col].mean()

    wide = tmp.pivot(index=subject_col, columns=time_col, values=value_col)

    if time_order is not None:
        wide = wide[[col for col in time_order if col in wide.columns]]

    complete = wide.dropna()

    if complete.shape[0] < 3 or complete.shape[1] < 2:
        return {
            "Dataset": dataset_name,
            "Variable": variable,
            "N_Subjects_Complete": complete.shape[0],
            "N_Timepoints": complete.shape[1],
            "Timepoints": ", ".join(map(str, complete.columns)),
            "F": np.nan,
            "Num_DF": np.nan,
            "Den_DF": np.nan,
            "p_value": np.nan,
            "Partial_Eta_Squared": np.nan,
            "Status": "Insufficient complete repeated measures",
        }

    long_df = complete.reset_index().melt(
        id_vars=subject_col, var_name=time_col, value_name="Value"
    )

    try:
        model = AnovaRM(
            long_df,
            depvar="Value",
            subject=subject_col,
            within=[time_col],
        ).fit()

        table = model.anova_table.reset_index()
        row = table.iloc[0]

        f_value = row.get("F Value", np.nan)
        num_df = row.get("Num DF", np.nan)
        den_df = row.get("Den DF", np.nan)
        p_value = row.get("Pr > F", np.nan)

        if pd.notna(f_value) and pd.notna(num_df) and pd.notna(den_df):
            partial_eta_squared = (f_value * num_df) / (f_value * num_df + den_df)
        else:
            partial_eta_squared = np.nan

        return {
            "Dataset": dataset_name,
            "Variable": variable,
            "N_Subjects_Complete": complete.shape[0],
            "N_Timepoints": complete.shape[1],
            "Timepoints": ", ".join(map(str, complete.columns)),
            "F": f_value,
            "Num_DF": num_df,
            "Den_DF": den_df,
            "p_value": p_value,
            "Partial_Eta_Squared": partial_eta_squared,
            "Status": "OK",
        }

    except Exception as exc:
        return {
            "Dataset": dataset_name,
            "Variable": variable,
            "N_Subjects_Complete": complete.shape[0],
            "N_Timepoints": complete.shape[1],
            "Timepoints": ", ".join(map(str, complete.columns)),
            "F": np.nan,
            "Num_DF": np.nan,
            "Den_DF": np.nan,
            "p_value": np.nan,
            "Partial_Eta_Squared": np.nan,
            "Status": f"ANOVA failed: {str(exc)[:120]}",
        }


def run_time_anovas(inspiration4, bedrest_wide):
    """Run repeated-measures ANOVA for I4 and Bed Rest using final 18 variables."""
    i4_rows = []
    br_rows = []
    crp_log_rows = []

    i4_time_order = ["L-92", "L-44", "L-3", "R+1", "R+45", "R+82", "R+194"]
    br_time_order = ["BR_Pre", "BR_In", "BR_Post"]

    for variable in FINAL_18_VARIABLES:
        # Inspiration4 raw ANOVA
        i4_col = I4_COLUMN_MAP.get(variable)
        if i4_col is not None and i4_col in inspiration4.columns:
            i4_rows.append(
                run_rm_anova_complete_cases(
                    inspiration4,
                    subject_col="Subject_ID",
                    time_col="Timepoint",
                    value_col=i4_col,
                    dataset_name="Inspiration4",
                    variable=variable,
                    time_order=i4_time_order,
                )
            )
        else:
            i4_rows.append(
                {
                    "Dataset": "Inspiration4",
                    "Variable": variable,
                    "N_Subjects_Complete": 0,
                    "N_Timepoints": 0,
                    "Timepoints": "",
                    "F": np.nan,
                    "Num_DF": np.nan,
                    "Den_DF": np.nan,
                    "p_value": np.nan,
                    "Partial_Eta_Squared": np.nan,
                    "Status": "Variable not present in Inspiration4 file",
                }
            )

        # Bed Rest raw ANOVA
        br_col = BR_VARIABLE_MAP.get(variable)
        if br_col is not None and br_col in bedrest_wide.columns:
            br_rows.append(
                run_rm_anova_complete_cases(
                    bedrest_wide,
                    subject_col="Subject_ID",
                    time_col="Phase_Group",
                    value_col=br_col,
                    dataset_name="Bed Rest",
                    variable=variable,
                    time_order=br_time_order,
                )
            )
        else:
            br_rows.append(
                {
                    "Dataset": "Bed Rest",
                    "Variable": variable,
                    "N_Subjects_Complete": 0,
                    "N_Timepoints": 0,
                    "Timepoints": "",
                    "F": np.nan,
                    "Num_DF": np.nan,
                    "Den_DF": np.nan,
                    "p_value": np.nan,
                    "Partial_Eta_Squared": np.nan,
                    "Status": "Variable not present or derivable in Bed Rest file",
                }
            )

    # CRP log10 ANOVA.
    # A small offset is not added here. Values <=0 are set to NaN before log10.
    if I4_COLUMN_MAP["CRP"] in inspiration4.columns:
        i4_log = inspiration4.copy()
        crp = safe_numeric(i4_log[I4_COLUMN_MAP["CRP"]])
        i4_log["CRP_log10"] = np.where(crp > 0, np.log10(crp), np.nan)

        crp_log_rows.append(
            run_rm_anova_complete_cases(
                i4_log,
                subject_col="Subject_ID",
                time_col="Timepoint",
                value_col="CRP_log10",
                dataset_name="Inspiration4",
                variable="CRP_log10",
                time_order=i4_time_order,
            )
        )

    if BR_VARIABLE_MAP["CRP"] in bedrest_wide.columns:
        br_log = bedrest_wide.copy()
        crp = safe_numeric(br_log[BR_VARIABLE_MAP["CRP"]])
        br_log["CRP_log10"] = np.where(crp > 0, np.log10(crp), np.nan)

        crp_log_rows.append(
            run_rm_anova_complete_cases(
                br_log,
                subject_col="Subject_ID",
                time_col="Phase_Group",
                value_col="CRP_log10",
                dataset_name="Bed Rest",
                variable="CRP_log10",
                time_order=br_time_order,
            )
        )

    i4_anova = apply_bh_fdr(pd.DataFrame(i4_rows), p_col="p_value", out_col="FDR_BH")
    br_anova = apply_bh_fdr(pd.DataFrame(br_rows), p_col="p_value", out_col="FDR_BH")
    crp_log_anova = apply_bh_fdr(
        pd.DataFrame(crp_log_rows), p_col="p_value", out_col="FDR_BH"
    )

    return i4_anova, br_anova, crp_log_anova


def timepoint_descriptives(inspiration4, bedrest_wide):
    """Generate timepoint descriptive statistics for all final 18 variables."""
    rows = []

    for variable in FINAL_18_VARIABLES:
        i4_col = I4_COLUMN_MAP.get(variable)
        if i4_col is not None and i4_col in inspiration4.columns:
            tmp = inspiration4[["Subject_ID", "Timepoint", i4_col]].copy()
            tmp[i4_col] = safe_numeric(tmp[i4_col])

            for timepoint, group in tmp.dropna(subset=[i4_col]).groupby("Timepoint"):
                ci_low, ci_high = mean_ci_95(group[i4_col])

                rows.append(
                    {
                        "Dataset": "Inspiration4",
                        "Variable": variable,
                        "Timepoint": timepoint,
                        "N": group[i4_col].count(),
                        "Mean": group[i4_col].mean(),
                        "SD": group[i4_col].std(ddof=1),
                        "Median": group[i4_col].median(),
                        "CI95_Low": ci_low,
                        "CI95_High": ci_high,
                    }
                )

        br_col = BR_VARIABLE_MAP.get(variable)
        if br_col is not None and br_col in bedrest_wide.columns:
            tmp = bedrest_wide[["Subject_ID", "Phase_Group", br_col]].copy()
            tmp[br_col] = safe_numeric(tmp[br_col])

            for phase, group in tmp.dropna(subset=[br_col]).groupby("Phase_Group"):
                ci_low, ci_high = mean_ci_95(group[br_col])

                rows.append(
                    {
                        "Dataset": "Bed Rest",
                        "Variable": variable,
                        "Timepoint": phase,
                        "N": group[br_col].count(),
                        "Mean": group[br_col].mean(),
                        "SD": group[br_col].std(ddof=1),
                        "Median": group[br_col].median(),
                        "CI95_Low": ci_low,
                        "CI95_High": ci_high,
                    }
                )

    return pd.DataFrame(rows)


def clinical_flags(group_summary):
    """Identify cohort-level mean z-score deviations from NHANES."""
    flagged = group_summary.copy()

    flagged["Flag_abs_mean_z_ge_1"] = flagged["Mean_Z"].abs() >= 1
    flagged["Flag_abs_mean_z_ge_1_96"] = flagged["Mean_Z"].abs() >= 1.96
    flagged["Flag_abs_mean_z_ge_2"] = flagged["Mean_Z"].abs() >= 2

    keep = flagged[
        ["Flag_abs_mean_z_ge_1", "Flag_abs_mean_z_ge_1_96", "Flag_abs_mean_z_ge_2"]
    ].any(axis=1)

    return flagged[keep].copy()


def significant_findings(group_summary, pairwise, i4_anova, br_anova, crp_log_anova):
    """Assemble FDR-significant findings across statistical analyses."""
    significant_vs_nhanes = group_summary[
        group_summary["FDR_BH_vs_NHANES_0"].lt(0.05).fillna(False)
    ].copy()
    significant_vs_nhanes["Analysis"] = "Group vs NHANES z=0"

    significant_pairwise = pairwise[pairwise["FDR_BH"].lt(0.05).fillna(False)].copy()
    significant_pairwise["Analysis"] = "Pairwise z-score comparison"

    significant_i4_anova = i4_anova[i4_anova["FDR_BH"].lt(0.05).fillna(False)].copy()
    significant_i4_anova["Analysis"] = "I4 repeated-measures ANOVA"

    significant_br_anova = br_anova[br_anova["FDR_BH"].lt(0.05).fillna(False)].copy()
    significant_br_anova["Analysis"] = "BR repeated-measures ANOVA"

    significant_crp_log = crp_log_anova[
        crp_log_anova["FDR_BH"].lt(0.05).fillna(False)
    ].copy()
    significant_crp_log["Analysis"] = "CRP log10 repeated-measures ANOVA"

    return pd.concat(
        [
            significant_vs_nhanes,
            significant_pairwise,
            significant_i4_anova,
            significant_br_anova,
            significant_crp_log,
        ],
        ignore_index=True,
        sort=False,
    )


def methods_table():
    """Create workbook README/methods table."""
    return pd.DataFrame(
        {
            "Section": [
                "Alpha",
                "FDR threshold",
                "Final overlap panel",
                "NHANES reference",
                "Z-score formula",
                "Inspiration4 pooled groups",
                "Bed Rest groups",
                "Group vs NHANES tests",
                "Pairwise cohort tests",
                "Repeated-measures ANOVA",
                "CRP analysis",
                "Effect sizes",
                "Multiple comparison correction",
            ],
            "Description": [
                "Nominal alpha was set to 0.05 for all statistical tests.",
                "Benjamini-Hochberg FDR-adjusted q < 0.05 was used as the primary significance threshold.",
                "Analyses were restricted to 18 overlapping biochemical measures: albumin, albumin/globulin ratio, alkaline phosphatase, ALT, AST, total bilirubin, BUN, BUN/creatinine ratio, calcium, carbon dioxide, chloride, creatinine, CRP, globulin, glucose, potassium, total protein, and sodium.",
                "NHANES mean and SD were calculated for each available overlap variable and used as the terrestrial reference distribution.",
                "z = (individual raw value - NHANES mean) / NHANES SD.",
                "I4_Pre pools L-92, L-44, and L-3; I4_Post pools R+1, R+45, R+82, and R+194.",
                "BR_Pre, BR_In, and BR_Post correspond to PRE_TEST, IN_TEST, and POST_TEST.",
                "One-sample t-tests evaluated whether each cohort mean z-score differed from 0.",
                "Welch t-tests were used for independent Bed Rest vs Inspiration4 comparisons. Paired t-tests were used for within-cohort comparisons with repeated subject IDs.",
                "Repeated-measures ANOVA was performed separately for Inspiration4 across all mission timepoints and Bed Rest across Pre/In/Post phases using complete cases.",
                "CRP repeated-measures ANOVA was performed on raw CRP and log10(CRP), with nonpositive CRP values treated as missing for log transformation.",
                "Hedges' g was reported for independent comparisons; Cohen's dz was reported for paired comparisons.",
                "Benjamini-Hochberg correction was applied separately within major statistical test tables.",
            ],
        }
    )


def write_workbook(
    output_file,
    methods,
    mapping_status,
    nhanes_reference,
    group_summary,
    pairwise,
    flags,
    significant,
    zscores,
    i4_anova,
    br_anova,
    crp_log_anova,
    descriptives,
):
    """Write all analysis outputs to Excel."""
    with pd.ExcelWriter(output_file, engine="xlsxwriter") as writer:
        methods.to_excel(writer, sheet_name="README_Methods", index=False)
        mapping_status.to_excel(writer, sheet_name="Final18_Mapping", index=False)
        nhanes_reference.to_excel(writer, sheet_name="NHANES_Reference", index=False)
        group_summary.to_excel(writer, sheet_name="ZScore_Group_Summary", index=False)
        pairwise.to_excel(writer, sheet_name="Cohort_Pairwise_Tests", index=False)
        flags.to_excel(writer, sheet_name="Clinical_Flags", index=False)
        significant.to_excel(writer, sheet_name="Significant_Findings", index=False)
        zscores.to_excel(writer, sheet_name="Individual_ZScores", index=False)
        i4_anova.to_excel(writer, sheet_name="I4_RM_ANOVA_Time", index=False)
        br_anova.to_excel(writer, sheet_name="BR_RM_ANOVA_Time", index=False)
        crp_log_anova.to_excel(writer, sheet_name="CRP_Log10_RM_ANOVA", index=False)
        descriptives.to_excel(writer, sheet_name="Timepoint_Descriptives", index=False)

        workbook = writer.book
        header_fmt = workbook.add_format(
            {"bold": True, "bg_color": "#D9EAF7", "border": 1}
        )
        num_fmt = workbook.add_format({"num_format": "0.000"})
        sci_fmt = workbook.add_format({"num_format": "0.000E+00"})

        dfs = {
            "README_Methods": methods,
            "Final18_Mapping": mapping_status,
            "NHANES_Reference": nhanes_reference,
            "ZScore_Group_Summary": group_summary,
            "Cohort_Pairwise_Tests": pairwise,
            "Clinical_Flags": flags,
            "Significant_Findings": significant,
            "Individual_ZScores": zscores,
            "I4_RM_ANOVA_Time": i4_anova,
            "BR_RM_ANOVA_Time": br_anova,
            "CRP_Log10_RM_ANOVA": crp_log_anova,
            "Timepoint_Descriptives": descriptives,
        }

        for sheet_name, df in dfs.items():
            worksheet = writer.sheets[sheet_name]
            worksheet.freeze_panes(1, 0)

            if len(df.columns) > 0:
                worksheet.autofilter(0, 0, max(len(df), 1), len(df.columns) - 1)

            for col_idx, col_name in enumerate(df.columns):
                width = min(max(len(str(col_name)) + 2, 12), 36)

                if col_name in {
                    "Description",
                    "Status",
                    "Analysis",
                    "Comparison",
                    "Variable",
                    "Timepoints",
                }:
                    width = min(max(width, 30), 90)

                if col_name == "Description":
                    width = 100

                worksheet.write(0, col_idx, col_name, header_fmt)

                if any(term in col_name.lower() for term in ["p_value", "fdr"]):
                    worksheet.set_column(col_idx, col_idx, max(width, 14), sci_fmt)
                elif any(
                    term in col_name.lower()
                    for term in [
                        "mean",
                        "sd",
                        "median",
                        "ci95",
                        "z",
                        "effect",
                        "statistic",
                        "eta",
                        "percentile",
                        "value",
                        "raw",
                        "f",
                    ]
                ):
                    worksheet.set_column(col_idx, col_idx, max(width, 14), num_fmt)
                else:
                    worksheet.set_column(col_idx, col_idx, width)


def run_pipeline(args):
    """Run complete LUNAR statistical comparison pipeline."""
    nhanes = pd.read_csv(args.nhanes_csv, low_memory=False)
    inspiration4 = pd.read_csv(args.inspiration4_wide)
    bedrest = pd.read_excel(args.bedrest_long, sheet_name=args.bedrest_sheet)

    nhanes = add_derived_nhanes_variables(nhanes)
    nhanes_map = read_nhanes_overlap_map(args.nhanes_overlap)
    bedrest_wide = prepare_bedrest_wide(bedrest)

    nhanes_reference = make_nhanes_reference(nhanes, nhanes_map)
    mapping_status = build_mapping_status(nhanes_reference, inspiration4, bedrest_wide)

    zscores = build_individual_zscores(inspiration4, bedrest_wide, nhanes_reference)
    group_summary = summarize_groups(zscores)
    pairwise = pairwise_tests(zscores)

    i4_anova, br_anova, crp_log_anova = run_time_anovas(inspiration4, bedrest_wide)
    descriptives = timepoint_descriptives(inspiration4, bedrest_wide)

    flags = clinical_flags(group_summary)
    significant = significant_findings(
        group_summary, pairwise, i4_anova, br_anova, crp_log_anova
    )

    methods = methods_table()

    write_workbook(
        output_file=args.output,
        methods=methods,
        mapping_status=mapping_status,
        nhanes_reference=nhanes_reference,
        group_summary=group_summary,
        pairwise=pairwise,
        flags=flags,
        significant=significant,
        zscores=zscores,
        i4_anova=i4_anova,
        br_anova=br_anova,
        crp_log_anova=crp_log_anova,
        descriptives=descriptives,
    )

    print(f"Saved workbook: {args.output}")
    print(f"Final overlap variables: {len(FINAL_18_VARIABLES)}")
    print(f"Individual z-score rows: {len(zscores)}")
    print(f"Group summary rows: {len(group_summary)}")
    print(f"Pairwise test rows: {len(pairwise)}")
    print(f"I4 ANOVA rows: {len(i4_anova)}")
    print(f"BR ANOVA rows: {len(br_anova)}")
    print(f"CRP log10 ANOVA rows: {len(crp_log_anova)}")
    print(f"Output size: {os.path.getsize(args.output) / 1024 / 1024:.2f} MB")


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate LUNAR final 18 statistical comparison workbook."
    )

    parser.add_argument(
        "--nhanes-csv",
        default="nhanes_biopro_all_cycles_combined.csv",
        help="Path to combined NHANES biochemical profile CSV.",
    )
    parser.add_argument(
        "--nhanes-overlap",
        default="LUNAR_NHANES_OVERLAP_Summary_v2.xlsx",
        help="Path to NHANES overlap/crosswalk workbook.",
    )
    parser.add_argument(
        "--inspiration4-wide",
        default="Inspiration4_Master_Wide.csv",
        help="Path to Inspiration4 individual-level wide CSV.",
    )
    parser.add_argument(
        "--bedrest-long",
        default="Campaign1_Master_Long_REAL.xlsx",
        help="Path to Bed Rest Campaign 1 individual-level long workbook.",
    )
    parser.add_argument(
        "--bedrest-sheet",
        default="Master_Long",
        help="Sheet name in Bed Rest workbook containing long-format data.",
    )
    parser.add_argument(
        "--output",
        default="LUNAR_Final18_Statistical_Comparison_Workbook.xlsx",
        help="Output Excel workbook path.",
    )

    return parser.parse_args()


if __name__ == "__main__":
    run_pipeline(parse_args())
