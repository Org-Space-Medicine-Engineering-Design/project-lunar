#!/usr/bin/env python3
"""
generate_zscore_heatmaps.py

Generate the final combined mean/median NHANES-referenced z-score heatmap figure
from LUNAR_Final18_Statistical_Comparison_Workbook.xlsx.

Output:
  Figure_01_Zscore_Heatmaps.png
"""

from pathlib import Path
import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


DEFAULT_GROUP_ORDER = ["BR_Pre", "BR_In", "BR_Post", "I4_Pre", "I4_Post"]
DEFAULT_GROUP_LABELS = {
    "BR_Pre": "BR Pre\n(n=9)",
    "BR_In": "BR In\n(n=9)",
    "BR_Post": "BR Post\n(n=9)",
    "I4_Pre": "I4 Pre\n(n=4)",
    "I4_Post": "I4 Post\n(n=4)",
}

DISPLAY_NAMES = {
    "ALBUMIN": "Albumin",
    "ALBUMIN/GLOBULIN RATIO": "Albumin/Globulin Ratio",
    "ALKALINE PHOSPHATASE": "Alkaline Phosphatase",
    "ALT": "ALT",
    "AST": "AST",
    "BILIRUBIN; TOTAL": "Bilirubin, Total",
    "BUN": "BUN",
    "BUN/CREATININE RATIO": "BUN/Creatinine Ratio",
    "CALCIUM": "Calcium",
    "CARBON DIOXIDE": "Carbon Dioxide",
    "CHLORIDE": "Chloride",
    "CREATININE": "Creatinine",
    "GLOBULIN": "Globulin",
    "GLUCOSE": "Glucose",
    "POTASSIUM": "Potassium",
    "PROTEIN; TOTAL": "Protein, Total",
    "SODIUM": "Sodium",
}

VARIABLE_ORDER = [
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
    "GLOBULIN",
    "GLUCOSE",
    "POTASSIUM",
    "PROTEIN; TOTAL",
    "SODIUM",
]


def build_matrix(summary: pd.DataFrame, metric: str) -> pd.DataFrame:
    df = summary.copy()
    df = df[df["Variable"].isin(VARIABLE_ORDER)]
    mat = df.pivot_table(index="Variable", columns="Cohort_Group", values=metric, aggfunc="mean")
    mat = mat.reindex(index=VARIABLE_ORDER, columns=DEFAULT_GROUP_ORDER)
    mat.index = [DISPLAY_NAMES.get(v, v) for v in mat.index]
    mat.columns = [DEFAULT_GROUP_LABELS.get(c, c) for c in mat.columns]
    return mat


def draw_heatmap(ax, mat: pd.DataFrame, title: str, footnote: str):
    vmax = 3
    vmin = -3.5
    im = ax.imshow(mat.values, cmap="bwr", vmin=vmin, vmax=vmax, aspect="auto")

    ax.set_title(title, fontsize=18, weight="bold", pad=18)
    ax.set_xticks(np.arange(mat.shape[1]))
    ax.set_xticklabels(mat.columns, fontsize=10, weight="bold")
    ax.set_yticks(np.arange(mat.shape[0]))
    ax.set_yticklabels(mat.index, fontsize=10)
    ax.tick_params(top=True, bottom=False, labeltop=True, labelbottom=False)

    for i in range(mat.shape[0]):
        for j in range(mat.shape[1]):
            val = mat.iloc[i, j]
            if pd.notna(val):
                ax.text(j, i, f"{val:.2f}", ha="center", va="center", fontsize=9, weight="bold", color="black")

    ax.set_xlabel("Cohort / Phase", fontsize=11, weight="bold", labelpad=16)
    ax.xaxis.set_label_position("bottom")
    ax.tick_params(labelbottom=False)

    for spine in ax.spines.values():
        spine.set_visible(True)
        spine.set_linewidth(0.7)
        spine.set_color("0.45")

    ax.set_xticks(np.arange(-.5, mat.shape[1], 1), minor=True)
    ax.set_yticks(np.arange(-.5, mat.shape[0], 1), minor=True)
    ax.grid(which="minor", color="0.82", linestyle="-", linewidth=0.5)
    ax.tick_params(which="minor", bottom=False, left=False)

    cbar = plt.colorbar(im, ax=ax, fraction=0.045, pad=0.03)
    cbar.set_label("Z-score (vs. NHANES Reference)", fontsize=11, weight="bold")
    cbar.ax.tick_params(labelsize=9)

    ax.text(0, -0.08, footnote, transform=ax.transAxes, ha="left", va="top", fontsize=8)
    return im


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="LUNAR_Final18_Statistical_Comparison_Workbook.xlsx")
    parser.add_argument("--output", default="Figure_01_Zscore_Heatmaps.png")
    args = parser.parse_args()

    summary = pd.read_excel(args.input, sheet_name="ZScore_Group_Summary")

    # CRP intentionally excluded from final heatmap because NHANES Mahalanobis panel is 17 biomarkers.
    summary = summary[summary["Variable"].ne("CRP")].copy()

    mean_mat = build_matrix(summary, "Mean_Z")
    median_mat = build_matrix(summary, "Median_Z")

    plt.rcParams.update({
        "font.family": "Arial",
        "font.size": 10,
    })

    fig, axes = plt.subplots(1, 2, figsize=(16, 9), constrained_layout=False)

    draw_heatmap(
        axes[0],
        mean_mat,
        "Mean NHANES-Referenced Z-Scores",
        "Values represent cohort mean NHANES-referenced z-scores.\nPositive values indicate higher than NHANES reference; negative values indicate lower.",
    )
    draw_heatmap(
        axes[1],
        median_mat,
        "Median NHANES-Referenced Z-Scores",
        "Values represent cohort median NHANES-referenced z-scores.\nPositive values indicate higher than NHANES reference; negative values indicate lower.",
    )

    fig.tight_layout(w_pad=4)
    fig.savefig(args.output, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {args.output}")


if __name__ == "__main__":
    main()
