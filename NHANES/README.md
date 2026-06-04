# NHANES BIOPRO Dataset for LUNAR

This folder contains the NHANES BIOPRO chemistry dataset and derived LUNAR summary workbooks used as a terrestrial reference population for comparison against Inspiration4, bed-rest campaigns, and future astronaut or analog cohorts.

## Purpose

The goal of this NHANES BIOPRO pull is to create a clean, cross-sectional terrestrial reference dataset focused on serum biochemistry variables that overlap with LUNAR spaceflight and bed-rest datasets. Unlike the earlier NHANES first pull, which emphasized demographics, CBC, lipids, diet, supplements, cotinine, and urine albumin/creatinine variables, this BIOPRO pull focuses on clinical chemistry analytes that are directly comparable to the chemistry portion of Inspiration4 and bed-rest datasets.

NHANES is used here as a terrestrial reference population, not as a spaceflight analog.

## Key Conceptual Notes

- `SEQN` is the NHANES participant/subject identifier.
- `SEQN` is not a measured laboratory variable and should be excluded from variable statistics, variability calculations, and missingness-by-variable summaries.
- NHANES BIOPRO is cross-sectional for the purposes of this LUNAR workbook.
- No timepoint-based summaries are generated for NHANES.
- Some NHANES cycles include second-exam or repeat-measurement variables; these are retained in the all-cycles combined file but are not treated as longitudinal timepoints.

## Main Files

### Processed CSV Files

`processed_csv/nhanes_biopro_all_cycles_combined.csv`  
All-cycles NHANES BIOPRO chemistry dataset. BIOPRO files from multiple NHANES cycles were concatenated by rows using `SEQN` as the participant identifier. Provenance columns were added for `nhanes_cycle`, `source_file`, and `exam_type`.

`processed_csv/LUNAR_NHANES_OVERLAP_Data_Wide_v2.csv`  
NHANES-only overlap-ready dataset containing only the selected chemistry variables expected to overlap with Inspiration4 and/or bed-rest chemistry datasets, plus derived ratios.

### Summary Workbooks

`summaries/LUNAR_NHANES_Data_Quality_Summary_v4.xlsx`  
NHANES BIOPRO data-quality summary workbook. Includes dataset inventory, variable statistics, inter-subject variability, missingness by variable, missingness by participant, units audit, and naming audit.

`summaries/LUNAR_NHANES_OVERLAP_Summary_v2.xlsx`  
NHANES-only overlap summary workbook. Includes only the overlap chemistry variables and derived ratios, using the same general structure as the LUNAR Inspiration4 and Bed Rest overlap workbooks.

### Scripts

`scripts/build_nhanes_biopro_all_cycles_combined.py`  
Builds `nhanes_biopro_all_cycles_combined.csv` from raw NHANES BIOPRO XPT files.

`scripts/build_lunar_nhanes_data_quality_summary.py`  
Builds `LUNAR_NHANES_Data_Quality_Summary_v4.xlsx` from the all-cycles combined BIOPRO CSV.

`scripts/build_lunar_nhanes_overlap_summary.py`  
Builds `LUNAR_NHANES_OVERLAP_Summary_v2.xlsx` and `LUNAR_NHANES_OVERLAP_Data_Wide_v2.csv` from the all-cycles combined BIOPRO CSV.

## BIOPRO Source Files Used

The combined NHANES BIOPRO dataset was created by row-stacking the following public-use BIOPRO files:

| NHANES Cycle | Source File | Exam Type |
|---|---|---|
| 1999-2000 | `LAB18.xpt` | main |
| 2001-2002 | `L40_B.xpt` | main |
| 2001-2002 | `L40_2_B.xpt` | second_exam |
| 2003-2004 | `L40_C.xpt` | main |
| 2005-2006 | `BIOPRO_D.xpt` | main |
| 2009-2010 | `BIOPRO_F.xpt` | main |
| 2011-2012 | `BIOPRO_G.xpt` | main |
| 2013-2014 | `BIOPRO_H.xpt` | main |
| 2015-2016 | `BIOPRO_I.xpt` | main |
| 2017-2018 | `BIOPRO_J.xpt` | main |
| 2017-March 2020 | `P_BIOPRO.xpt` | main_pre_pandemic |

## How the BIOPRO Combined File Was Created

The BIOPRO combined file was created by adapting the original NHANES first-pull workflow. The first pull merged multiple NHANES domains by `SEQN`; the BIOPRO workflow instead concatenates a single laboratory domain across survey cycles.

Workflow:

1. Download NHANES BIOPRO public-use XPT files for available cycles.
2. Read each XPT file into Python using `pandas.read_sas(..., format="xport")`.
3. Add provenance columns:
   - `nhanes_cycle`
   - `source_file`
   - `exam_type`
4. Concatenate all BIOPRO files by rows.
5. Align variables by column name across cycles.
6. Preserve `SEQN` as the subject identifier.
7. Export the combined file as `nhanes_biopro_all_cycles_combined.csv`.

This produces a cross-sectional chemistry reference dataset with:

| Metric | Value |
|---|---:|
| Rows | 73,170 |
| Unique SEQN values | 72,624 |
| Duplicate SEQN rows | 546 |
| Columns | 91 |

The duplicate `SEQN` rows are expected and arise from the 2001-2002 second-exam BIOPRO file (`L40_2_B.xpt`).

## Data-Quality Summary Workbook

`LUNAR_NHANES_Data_Quality_Summary_v4.xlsx` contains the following sheets:

| Sheet | Description |
|---|---|
| `Dataset_Inventory` | Dataset-level row, subject, and variable counts. |
| `Variable_Stats` | Descriptive statistics for numeric variables, excluding `SEQN`. |
| `Inter_Subject_Variability` | Population variability using the same column structure as the LUNAR Inspiration4/Bed Rest summaries. |
| `Missing_By_Variable` | Missing count and percent for each variable, excluding `SEQN`. |
| `Missing_By_Participant` | Missing count and percent for each `SEQN` row. |
| `Units_Audit` | Variable units based on NHANES BIOPRO documentation. |
| `Naming_Audit` | Variable descriptions based on NHANES BIOPRO documentation. |

Because NHANES is cross-sectional in this context, the workbook does not include timepoint sheets such as `Missing_By_Timepoint`, `Subject_Timepoint_Stats`, or `Variable_Stats_By_Timepoint`.

## NHANES Overlap Summary Workbook

`LUNAR_NHANES_OVERLAP_Summary_v2.xlsx` contains the NHANES-only overlap subset. It is designed to mirror the structure of the LUNAR Inspiration4 and Bed Rest overlap workbooks while containing only NHANES values.

Included sheets:

| Sheet | Description |
|---|---|
| `Dataset_Inventory` | Summary of the NHANES overlap dataset. |
| `Variable_Stats` | Descriptive statistics for overlap variables only. |
| `Inter_Subject_Variability` | Population variability for overlap variables only. |
| `Missing_By_Variable` | Missingness for overlap variables only. |
| `Missing_By_Participant` | Participant-level missingness for overlap variables only. |
| `Units_Audit` | Units for overlap variables. |
| `Naming_Audit` | Descriptions and canonical names for overlap variables. |
| `Derived_Variables_Audit` | Formulas for derived overlap variables. |
| `Overlap_Data` | Preview of overlap-ready participant-level data. |

The full participant-level overlap dataset is exported separately as:

`processed_csv/LUNAR_NHANES_OVERLAP_Data_Wide_v2.csv`

## NHANES Overlap Variables

The NHANES overlap workbook includes 16 direct BIOPRO chemistry variables and 2 derived ratios.

### Direct Variables

| Canonical Variable | NHANES Variable | Unit |
|---|---|---|
| Albumin | `LBXSAL` | g/dL |
| Alkaline Phosphatase | `LBXSAPSI` | U/L |
| AST | `LBXSASSI` | U/L |
| ALT | `LBXSATSI` | U/L |
| BUN | `LBXSBU` | mg/dL |
| Carbon Dioxide / Bicarbonate | `LBXSC3SI` | mmol/L |
| Calcium | `LBXSCA` | mg/dL |
| Chloride | `LBXSCLSI` | mmol/L |
| Creatinine | `LBXSCR` | mg/dL |
| Globulin | `LBXSGB` | g/dL |
| Glucose | `LBXSGL` | mg/dL |
| Potassium | `LBXSKSI` | mmol/L |
| Sodium | `LBXSNASI` | mmol/L |
| Total Bilirubin | `LBXSTB` | mg/dL |
| Total Protein | `LBXSTP` | g/dL |
| Uric Acid | `LBXSUA` | mg/dL |

### Derived Variables

| Derived Variable | Formula | Unit |
|---|---|---|
| Albumin/Globulin Ratio | `LBXSAL / LBXSGB` | ratio |
| BUN/Creatinine Ratio | `LBXSBU / LBXSCR` | ratio |

## Recommended Use

Use `LUNAR_NHANES_Data_Quality_Summary_v4.xlsx` to inspect the full BIOPRO all-cycles chemistry dataset.

Use `LUNAR_NHANES_OVERLAP_Summary_v2.xlsx` and `LUNAR_NHANES_OVERLAP_Data_Wide_v2.csv` when comparing NHANES with Inspiration4, Bed Rest Campaign 1, or other LUNAR datasets.

## Relationship to the Original First Pull

The original NHANES first pull created a broad working dataset that included demographics, body measures, CBC, cotinine, urine albumin/creatinine, lipids, diet recalls, and supplement recalls. That dataset was useful for general NHANES exploration but did not contain the clinical chemistry variables needed for strong overlap with Inspiration4.

The BIOPRO pull was created to address that gap by focusing specifically on NHANES serum chemistry variables.

## Source Documentation

NHANES BIOPRO laboratory documentation/codebooks are available through the CDC/NCHS NHANES website. Example BIOPRO documentation page:

https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2017/DataFiles/BIOPRO_J.htm

