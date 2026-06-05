#!/usr/bin/env python3
"""
run_cross_dataset_analysis.py

Convenience runner for LUNAR cross-dataset analyses.

This does not replace the individual scripts. It simply calls them in a sensible
order with configurable paths.

Edit the CONFIG section below before running.
"""

from pathlib import Path
import subprocess
import sys

PYTHON = sys.executable

# -------------------------------------------------------------------------
# Edit these paths for your local repository
# -------------------------------------------------------------------------
NHANES_CSV = Path("processed_csv/nhanes_biopro_all_cycles_combined.csv")
NHANES_OVERLAP = Path("summaries/LUNAR_NHANES_OVERLAP_Summary_v2.xlsx")
I4_WIDE = Path("outputs/Inspiration4_Master_Wide.csv")
I4_OVERLAP = Path("summaries/LUNAR_Inspiration4_OVERLAP_Summary_v1.xlsx")
BR_OVERLAP = Path("summaries/LUNAR_BedRest_Campaign1_OVERLAP_Summary_v3.xlsx")
BR_LONG = Path("outputs/bed_rest_campaign1/LUNAR_BedRest_Campaign1_OVERLAP_v3_Master_Long.xlsx")
BR_SHEET = "Master_Long"

OUT_SUMMARY = Path("summaries/LUNAR_Final18_Statistical_Comparison_Workbook.xlsx")
MAHAL_OUTDIR = Path("outputs/mahalanobis_bootstrap")
ITERATIONS = 1000
SEED = 42

SCRIPT_DIR = Path(__file__).resolve().parent


def run(cmd):
    print("\nRUN:", " ".join(map(str, cmd)))
    subprocess.run(cmd, check=True)


def main():
    # 1. Final 18 statistical comparison workbook
    run([
        PYTHON,
        str(SCRIPT_DIR / "lunar_final18_statistical_comparison.py"),
        "--nhanes-csv", str(NHANES_CSV),
        "--nhanes-overlap", str(NHANES_OVERLAP),
        "--inspiration4-wide", str(I4_WIDE),
        "--bedrest-long", str(BR_LONG),
        "--bedrest-sheet", BR_SHEET,
        "--output", str(OUT_SUMMARY),
    ])

    # 2. Bootstrap Mahalanobis sensitivity analysis
    run([
        PYTHON,
        str(SCRIPT_DIR / "mahalanobis_nhanes_i4_br.py"),
        "--nhanes", str(NHANES_CSV),
        "--i4", str(I4_OVERLAP),
        "--br", str(BR_OVERLAP),
        "--outdir", str(MAHAL_OUTDIR),
        "--iterations", str(ITERATIONS),
        "--seed", str(SEED),
    ])

    # 3. Final real-data KDE figure
    # This script expects to run from the folder containing mahalanobis_distance_summary.xlsx.
    run([
        PYTHON,
        str(SCRIPT_DIR / "generate_realdata_kde_no_phase_titles.py"),
    ])

    print("\nCross-dataset analysis complete.")


if __name__ == "__main__":
    main()
