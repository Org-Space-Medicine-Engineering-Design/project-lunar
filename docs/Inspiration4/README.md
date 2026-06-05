# Inspiration4 Biomedical Dataset

## Overview

This folder contains the Inspiration4 cohort datasets, processing scripts, derived datasets, harmonization products, and quality-control reports generated as part of the **LUNAR (Longitudinal Unification of Small-N Astronaut Responses)** project.

The purpose of this dataset is to create analysis-ready longitudinal biomedical data products from the Inspiration4 mission that can be compared with terrestrial reference populations (e.g., NHANES) and spaceflight analog cohorts (e.g., UTMB Bed Rest Campaigns).

The Inspiration4 dataset serves as the first astronaut cohort integrated into the LUNAR framework and provides the foundation for future cross-cohort harmonization efforts.

---

# Source Data

The integrated datasets were generated from the following Inspiration4 source files.

## Clinical Chemistry

* LSDS-8_Comprehensive_Metabolic_Panel_CMP.upload_SUBMITTED.csv

## Multiplex Biomarker Panels

* LSDS-8_Multiplex_serum.cardiovascular.EvePanel_SUBMITTED.csv
* LSDS-8_Multiplex_serum.immune.EvePanel_SUBMITTED.csv
* LSDS-8_Multiplex_serum.immune.AlamarPanel_SUBMITTED.xlsx

## Demographics

* Demographics_inspiration4.xlsx

These datasets include:

* Clinical chemistry measurements
* Immune biomarkers
* Cytokines
* Cardiovascular biomarkers
* Demographic information
* Longitudinal sampling timepoints

---

# Processing Pipeline

## combine_inspiration4_data.py

This script:

1. Loads all source datasets.
2. Standardizes variable names.
3. Harmonizes participant identifiers.
4. Harmonizes collection timepoints.
5. Merges demographic information.
6. Combines clinical chemistry, immune, and cardiovascular biomarker panels into a unified structure.
7. Generates analysis-ready long-format and wide-format datasets.

Run:

```bash
py scripts/combine_inspiration4_data.py
```

Outputs:

* Inspiration4_Master_Long.csv
* Inspiration4_Master_Wide.csv

---

## summary_statistics_inspiration4_v2.py

This script generates quality-control and harmonization workbooks from the integrated master datasets.

Inputs:

* Inspiration4_Master_Wide.csv
* Inspiration4_Master_Long.csv
* Demographics_inspiration4.xlsx

The script reconstructs a longitudinal data structure from the master datasets and produces:

1. A comprehensive Inspiration4 quality-control workbook.
2. A harmonized overlap workbook containing approved overlap variables shared with Bed Rest and NHANES harmonization efforts.

Run:

```bash
py scripts/summary_statistics_inspiration4_v2.py \
    --wide outputs/Inspiration4_Master_Wide.csv \
    --long outputs/Inspiration4_Master_Long.csv \
    --demographics data/raw/Inspiration4/Demographics_inspiration4.xlsx \
    --out outputs/Inspiration4_Data_Quality_Summary_V2.xlsx \
    --overlap-out outputs/LUNAR_Inspiration4_OVERLAP_Summary_v1.xlsx
```

Outputs:

* Inspiration4_Data_Quality_Summary_V2.xlsx
* LUNAR_Inspiration4_OVERLAP_Summary_v1.xlsx

---

## generate_inspiration4_timepoint_binning.py

This script generates longitudinally binned astronaut datasets and cohort-level summary statistics from the Inspiration4 overlap workbook.

Input:

* LUNAR_Inspiration4_OVERLAP_Summary_v1.xlsx

Required sheet:

* Overlap_Data

Required columns:

* Subject_ID
* Variable
* Timepoint
* Value

Run:

```bash
python scripts/generate_inspiration4_timepoint_binning.py \
    --input outputs/LUNAR_Inspiration4_OVERLAP_Summary_v1.xlsx \
    --output outputs/Inspiration4_Timepoint_Binning_Workbook_All3_Summaries.xlsx
```

### Purpose

Different cohorts use different sampling schedules. This script generates multiple longitudinal binning strategies to facilitate direct comparison among:

* Inspiration4
* NHANES
* UTMB Bed Rest Campaigns
* Future LUNAR datasets

### Generated Workbook

Output:

* Inspiration4_Timepoint_Binning_Workbook_All3_Summaries.xlsx

The workbook contains one worksheet per overlap biomarker.

Each worksheet includes:

#### Raw Timepoint Data

Participant-level values for:

* L-92
* L-44
* L-3
* R+1
* R+45
* R+82
* R+194

---

#### Option 1: Mean Preflight vs Mean Postflight

Preflight:

* Mean(L-92, L-44, L-3)

Postflight:

* Mean(R+1, R+45, R+82, R+194)

Purpose:

* Primary longitudinal harmonization framework
* Reduces noise associated with individual collection days
* Supports cross-cohort comparisons

---

#### Option 2: Acute Response

Baseline:

* L-3

Postflight:

* R+1

Purpose:

* Captures immediate physiological response to spaceflight
* Supports acute-response comparisons

---

#### Option 3: Long-Term Recovery

Preflight:

* Mean(L-92, L-44, L-3)

Postflight:

* Mean(R+45, R+82, R+194)

Purpose:

* Excludes acute R+1 recovery effects
* Emphasizes longer-term physiological recovery

---

### Participant-Level Outputs

For each participant and variable:

* Baseline value
* Postflight value
* Delta
* Percent Delta
* Number of observations contributing to baseline estimate
* Number of observations contributing to postflight estimate

---

### Cohort Summary Sheets

The workbook generates three cohort-level summary worksheets.

#### Summary_Option1

Reports:

* Preflight Mean
* Preflight SD
* Postflight Mean
* Postflight SD
* Delta Mean
* Delta SD
* Percent Delta Mean
* Percent Delta SD
* N Subjects

#### Summary_Option2

Reports:

* L-3 Mean
* L-3 SD
* R+1 Mean
* R+1 SD
* Delta Mean
* Delta SD
* Percent Delta Mean
* Percent Delta SD
* N Subjects

#### Summary_Option3

Reports:

* Preflight Mean
* Preflight SD
* Long-Term Recovery Mean
* Long-Term Recovery SD
* Delta Mean
* Delta SD
* Percent Delta Mean
* Percent Delta SD
* N Subjects

---

# Available Outputs

## Inspiration4_Master_Long.csv

Integrated long-format dataset.

Characteristics:

* One row per measurement
* Preserves longitudinal structure
* Suitable for data exploration
* Suitable for harmonization workflows
* Suitable for longitudinal visualization

---

## Inspiration4_Master_Wide.csv

Integrated wide-format dataset.

Characteristics:

* One row per participant-timepoint
* Suitable for data integration
* Suitable for harmonization workflows
* Suitable for downstream dataset generation

---

## Inspiration4_Data_Quality_Summary_V2.xlsx

Comprehensive quality-control and cohort summary workbook.

Workbook tabs include:

* Dataset_Inventory
* Demographics
* Variable_Stats
* Variable_Stats_By_Timepoint
* Subject_Stats
* Subject_Timepoint_Variable_Stat
* Subject_Missingness
* Subject_Timepoint_Stats
* Missing_By_Variable
* Missing_By_Timepoint
* Missing_By_Participant
* Missing_By_Part_Time
* Units_Audit
* Naming_Audit
* Participant_Audit
* Inter_Subject_Variability
* Baseline_ISV
* Variable_Coverage
* Long_File_Variable_Inventory

Characteristics:

* Generated from integrated master datasets
* Provides quality-control reporting
* Provides coverage assessment
* Provides cohort characterization
* Supports harmonization planning

---

## LUNAR_Inspiration4_OVERLAP_Summary_v1.xlsx

Overlap workbook containing approved variables shared with Bed Rest and NHANES harmonization efforts.

Included variables:

* ALBUMIN
* ALKALINE PHOSPHATASE
* ALT
* AST
* BILIRUBIN; TOTAL
* CALCIUM
* CARBON DIOXIDE
* CHLORIDE
* CREATININE
* CRP
* GLUCOSE
* POTASSIUM
* PROTEIN; TOTAL
* SODIUM
* BUN
* UREA NITROGEN (BUN)
* GLOBULIN
* ALBUMIN/GLOBULIN RATIO
* BUN/CREATININE RATIO

Characteristics:

* Generated from Inspiration4 master datasets
* Uses a locked overlap-variable crosswalk
* Harmonized for Bed Rest comparison
* Harmonized for NHANES comparison
* Contains participant-level longitudinal overlap data

---

## Inspiration4_Timepoint_Binning_Workbook_All3_Summaries.xlsx

Longitudinal harmonization workbook generated from the overlap dataset.

Contains:

* One worksheet per overlap biomarker
* Raw participant-level timepoint data
* Three longitudinal binning strategies
* Three cohort-level summary worksheets
* Delta calculations
* Percent-change calculations

Primary use:

* Cross-cohort harmonization

---

# Cohort Summary

Mission:

* Inspiration4

Cohort Size:

* 4 participants

Primary Longitudinal Timepoints:

* L-92
* L-44
* L-3
* R+1
* R+45
* R+82
* R+194

Data Domains:

* Demographics
* Clinical chemistry
* Immune biomarkers
* Cytokines
* Cardiovascular biomarkers
* Inflammatory biomarkers

---

# Recommended Files

## Data Exploration

Use:

* Inspiration4_Master_Long.csv

Recommended uses:

* Review participant-level measurements
* Explore longitudinal trajectories
* Verify variable availability
* Assess timepoint coverage

---

## Data Integration and Harmonization

Use:

* Inspiration4_Master_Wide.csv

Recommended uses:

* Data integration
* Variable harmonization
* Cross-cohort alignment
* Dataset generation

---

## Data Quality Assessment

Use:

* Inspiration4_Data_Quality_Summary_V2.xlsx

Recommended uses:

* Missingness assessment
* Participant-level quality control
* Variable-level quality control
* Unit verification
* Cohort characterization

---

## Overlap Variable Assessment

Use:

* LUNAR_Inspiration4_OVERLAP_Summary_v1.xlsx

Recommended uses:

* Review overlap variables
* Verify harmonized biomarker mappings
* Compare variable availability across cohorts
* Support NHANES harmonization
* Support Bed Rest harmonization

---

## Longitudinal Harmonization

Use:

* Inspiration4_Timepoint_Binning_Workbook_All3_Summaries.xlsx

Recommended uses:

* Preflight-versus-postflight comparisons
* Acute-response assessment
* Long-term recovery assessment
* Cohort summary generation
* Cross-cohort harmonization

---

# Relationship to LUNAR

This dataset represents the first integrated astronaut cohort within the LUNAR project.

Future LUNAR harmonization efforts will compare Inspiration4 biomarker profiles with:

* NHANES terrestrial reference populations
* UTMB Bed Rest Campaigns
* Additional astronaut cohorts
* Additional biomedical datasets incorporated into the LUNAR framework

The longitudinal binning framework developed here serves as a harmonization bridge between astronaut, analog, and terrestrial datasets.

---

# Current Status

## Version 4.0

Completed:

* Data integration pipeline
* Demographic integration
* Long-format dataset generation
* Wide-format dataset generation
* Quality-control framework
* Overlap variable harmonization
* Locked overlap-variable crosswalk
* Longitudinal timepoint binning framework
* Acute-response binning framework
* Long-term recovery binning framework
* Cohort-level summary statistics generation
* Bed Rest harmonization framework
* NHANES harmonization framework
* LUNAR-compatible reporting framework

Current outputs:

* Inspiration4_Master_Long.csv
* Inspiration4_Master_Wide.csv
* Inspiration4_Data_Quality_Summary_V2.xlsx
* LUNAR_Inspiration4_OVERLAP_Summary_v1.xlsx
* Inspiration4_Timepoint_Binning_Workbook_All3_Summaries.xlsx

Status:

* Data integration complete
* Quality-control reporting complete
* Overlap harmonization complete
* Timepoint binning complete
* Cohort summary generation complete
* Harmonized for comparison with NHANES
* Harmonized for comparison with UTMB Bed Rest Campaigns
* Integrated into the LUNAR framework

---

# Citation

If using this dataset or derived products, please cite:

* The original Inspiration4 data source
* Associated Inspiration4 publications
* NASA Open Science Data Repository (OSDR) records where applicable
* Any downstream analyses generated from these integrated datasets

---

# Disclaimer

This folder contains derived datasets generated from publicly available Inspiration4 source data.

Users are responsible for:

* Verifying analyses
* Validating results
* Confirming interpretation of derived variables
* Ensuring compliance with original data-use requirements
