# Bed Rest Campaign 1 → Inspiration4 Overlap Summary

This folder contains the reproducible workflow used to generate the LUNAR Bed Rest Campaign 1 overlap summary workbook from the raw Campaign 1 bed rest CSV files.

LUNAR = **Longitudinal Unification of Small-N Astronaut Responses**.

## Purpose

The goal of this workflow is to identify and summarize the subset of Bed Rest Campaign 1 blood chemistry variables that overlap with variables measured in the Inspiration4 master long-format dataset. The output is intended to support later cross-dataset comparison among:

- Inspiration4
- Bed Rest Campaign 1
- NHANES

The current Bed Rest Campaign 1 overlap cohort is limited to the three clinical chemistry participants:

- `C1G0001`
- `C1G0002`
- `C1G0003`

Other raw subject identifiers appear in the full Campaign 1 files, but they come from non-overlap or group/sample-level files and are not included in the clinical chemistry overlap cohort.

## Inputs

The script requires only the raw Campaign 1 CSV files, either as:

1. A ZIP archive containing the 27 raw Campaign 1 CSV files, or
2. A directory containing the extracted CSV files.

Example input:

```text
Campaign 1-20260603T141236Z-3-001.zip
```

The Inspiration4 overlap variable mapping is embedded in the Python script. Therefore, the script does not require the Inspiration4 file to be present at runtime.

## Python requirements

Install the required Python packages:

```bash
pip install pandas numpy openpyxl
```

## How to run

From the repository root:

```bash
python scripts/build_bedrest_campaign1_overlap_summary.py \
  --input "data/raw/bed_rest_campaign1/Campaign 1-20260603T141236Z-3-001.zip" \
  --output-dir "outputs/bed_rest_campaign1" \
  --prefix "LUNAR_BedRest_Campaign1_OVERLAP_v3"
```

If the raw files are already extracted:

```bash
python scripts/build_bedrest_campaign1_overlap_summary.py \
  --input "data/raw/bed_rest_campaign1/Campaign 1" \
  --output-dir "outputs/bed_rest_campaign1" \
  --prefix "LUNAR_BedRest_Campaign1_OVERLAP_v3"
```

## Outputs

The script generates three files:

```text
LUNAR_BedRest_Campaign1_OVERLAP_v3_Summary.xlsx
LUNAR_BedRest_Campaign1_OVERLAP_v3_Overlap_Data.csv
LUNAR_BedRest_Campaign1_OVERLAP_v3_Master_Long.csv
```

### 1. Summary workbook

`LUNAR_BedRest_Campaign1_OVERLAP_v3_Summary.xlsx`

This is the main Excel workbook. It contains:

| Sheet | Description |
|---|---|
| `Dataset_Inventory` | High-level QC summary of cohort, variables, rows, and derivation rules |
| `Variable_Stats` | Overall summary statistics by variable |
| `Variable_Stats_By_Timepoint` | Summary statistics by variable and test phase |
| `Subject_Stats` | Summary statistics by subject and variable |
| `Subject_Timepoint_Variable_Stat` | Summary statistics by subject, test phase, and variable |
| `Subject_Missingness` | Missingness by subject |
| `Subject_Timepoint_Stats` | Variable coverage by subject and test phase |
| `Missing_By_Variable` | Missingness by variable |
| `Missing_By_Timepoint` | Missingness by PRE/IN/POST phase |
| `Overlap_Crosswalk` | Bed Rest-to-Inspiration4 overlap mapping |
| `Units_Audit` | Units observed for each overlap variable |
| `Derived_Variables_Audit` | Formulas and source files for derived variables |
| `Participant_Audit` | All raw subject IDs and whether they are included in the overlap cohort |
| `Overlap_Data` | Long-format overlap data used for the summary statistics |

### 2. Overlap data CSV

`LUNAR_BedRest_Campaign1_OVERLAP_v3_Overlap_Data.csv`

This is the analysis-ready long-format subset containing only the Inspiration4-overlap variables plus the derived variables.

### 3. Master long CSV

`LUNAR_BedRest_Campaign1_OVERLAP_v3_Master_Long.csv`

This is the full Campaign 1 long-format table created from all raw CSV files. It is useful for audit and troubleshooting but is not limited to the Inspiration4-overlap cohort.

## Variables included

The final overlap set contains 18 variables:

### Measured overlap variables

- `ALBUMIN`
- `ALKALINE PHOSPHATASE`
- `ALT`
- `AST`
- `BILIRUBIN; TOTAL`
- `CALCIUM`
- `CARBON DIOXIDE`
- `CHLORIDE`
- `CREATININE`
- `CRP`
- `GLUCOSE`
- `POTASSIUM`
- `PROTEIN; TOTAL`
- `SODIUM`
- `UREA NITROGEN (BUN)`

### Derived overlap variables

- `GLOBULIN`
- `ALBUMIN/GLOBULIN RATIO`
- `BUN/CREATININE RATIO`

## Derived variable rules

Three variables are calculated because they are present in the Inspiration4 dataset and can be derived from measured Bed Rest Campaign 1 blood chemistry values.

### Globulin

```text
GLOBULIN = PROTEIN; TOTAL - ALBUMIN
```

Unit: `g/dL`

### Albumin/globulin ratio

```text
ALBUMIN/GLOBULIN RATIO = ALBUMIN / GLOBULIN
```

Unit: `ratio`

### BUN/creatinine ratio

```text
BUN/CREATININE RATIO = UREA NITROGEN (BUN) / CREATININE
```

Unit: `ratio`

Important QC rule: `BUN/CREATININE RATIO` uses only the blood/serum creatinine measurement from the MR010G Flight Chemistry file. Urine creatinine and creatinine clearance are explicitly excluded.

## Participant-count clarification

The raw Campaign 1 master table contains many subject-like identifiers because different files include participant IDs, sample IDs, group IDs, and/or non-overlap study identifiers.

For the Inspiration4-overlap clinical chemistry dataset, the valid participant cohort is:

```text
C1G0001, C1G0002, C1G0003
```

The summary workbook therefore reports 3 overlap cohort participants. The `Participant_Audit` tab documents the raw subject identifiers found across all files and flags whether they are included in the overlap cohort.

## Missingness method

Missingness is calculated using expected coverage across:

```text
Subject × Test_Phase × Inspiration4-overlap Variable
```

Expected test phases are:

- `PRE_TEST`
- `IN_TEST`
- `POST_TEST`

A variable is considered present for a subject/timepoint if at least one numeric value exists for that subject, test phase, and variable.

## Summary statistics method

Summary statistics are calculated using numeric values only. The workbook reports:

- `N`
- `Mean`
- `SD`
- `Median`
- `Min`
- `Q1`
- `Q3`
- `IQR`
- `Max`

Non-numeric raw observations are retained in the master/overlap data where relevant for audit, but they do not contribute to numeric statistics.

## Recommended repository layout

```text
repo/
├── data/
│   └── raw/
│       └── bed_rest_campaign1/
│           └── Campaign 1-20260603T141236Z-3-001.zip
├── outputs/
│   └── bed_rest_campaign1/
├── scripts/
│   └── build_bedrest_campaign1_overlap_summary.py
└── README_bedrest_campaign1_overlap_summary.md
```

## Notes for future NHANES integration

The Bed Rest Campaign 1 workbook is now structured to support a three-way LUNAR comparison. The next step is to create a similar crosswalk for NHANES and define variables present in all three datasets:

```text
Inspiration4 ∩ Bed Rest Campaign 1 ∩ NHANES
```

