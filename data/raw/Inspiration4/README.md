# Inspiration4 Biomedical Dataset for LUNAR

## Overview

This folder contains the Inspiration4 astronaut biomedical datasets, processing scripts, harmonization products, overlap datasets, and quality-control reports generated as part of the LUNAR (Longitudinal Unification of Small-N Astronaut Responses) project.

The Inspiration4 dataset represents the first astronaut cohort integrated into the LUNAR framework and serves as the primary spaceflight cohort used for comparison with:

* NHANES terrestrial reference populations
* UTMB Bed Rest Campaign 1 analog participants
* Future astronaut and biomedical datasets incorporated into LUNAR

The objective of this workflow is to create harmonized, analysis-ready datasets that support longitudinal astronaut analyses and cross-cohort comparisons.

---

# Purpose

The Inspiration4 workflow was designed to:

1. Integrate multiple biomedical datasets collected during the Inspiration4 mission.
2. Harmonize participant identifiers and timepoints.
3. Generate longitudinal master datasets.
4. Quantify data completeness and quality.
5. Identify overlap biomarkers shared with NHANES and Bed Rest.
6. Generate longitudinal binning frameworks for cross-cohort comparisons.
7. Support NHANES-referenced z-score analyses.
8. Support Mahalanobis distance calculations within the LUNAR framework.

---

# Cohort Summary

Mission:

* Inspiration4

Participants:

* C001
* C002
* C003
* C004

Total Participants:

* 4

Primary Sampling Timepoints:

* L-92
* L-44
* L-3
* R+1
* R+45
* R+82
* R+194

Data Domains:

* Clinical chemistry
* Inflammatory biomarkers
* Immune biomarkers
* Cytokines
* Cardiovascular biomarkers
* Demographics

---

# Source Data

The integrated datasets were generated from the following Inspiration4 source files.

## Clinical Chemistry

* LSDS-8_Comprehensive_Metabolic_Panel_CMP.upload_SUBMITTED.csv

## Cardiovascular Biomarkers

* LSDS-8_Multiplex_serum.cardiovascular.EvePanel_SUBMITTED.csv

## Immune Biomarkers

* LSDS-8_Multiplex_serum.immune.EvePanel_SUBMITTED.csv

## Cytokine Biomarkers

* LSDS-8_Multiplex_serum.immune.AlamarPanel_SUBMITTED.xlsx

## Demographics

* Demographics_inspiration4.xlsx

---

# Main Outputs

## Inspiration4_Master_Long.csv

Integrated long-format dataset.

Characteristics:

* One row per measurement
* Preserves longitudinal structure
* Supports exploratory analysis
* Supports harmonization workflows
* Supports longitudinal visualization

---

## Inspiration4_Master_Wide.csv

Integrated wide-format dataset.

Characteristics:

* One row per participant-timepoint
* Supports data integration
* Supports harmonization workflows
* Supports overlap generation
* Supports statistical analysis

---

# Data Integration Workflow

## combine_inspiration4_data.py

This script performs the initial integration of all Inspiration4 datasets.

Processing steps:

1. Load all source datasets.
2. Standardize biomarker names.
3. Standardize participant identifiers.
4. Standardize collection timepoints.
5. Merge demographic information.
6. Harmonize chemistry and biomarker panels.
7. Generate long-format dataset.
8. Generate wide-format dataset.

Outputs:

```text
Inspiration4_Master_Long.csv
Inspiration4_Master_Wide.csv
```

---

# Data Quality Assessment

## Inspiration4_Data_Quality_Summary_v2_SubjectStats.xlsx

This workbook provides comprehensive quality-control reporting and cohort characterization.

Generated using:

```text
summary_statistics_inspiration4_v2_updated_with_overlap.py
```

Inputs:

```text
Inspiration4_Master_Long.csv
Inspiration4_Master_Wide.csv
Demographics_inspiration4.xlsx
```

Workbook contents:

| Worksheet                       | Description                       |
| ------------------------------- | --------------------------------- |
| Dataset_Inventory               | Dataset-level summary             |
| Demographics                    | Participant demographics          |
| Variable_Stats                  | Variable-level statistics         |
| Variable_Stats_By_Timepoint     | Timepoint-specific statistics     |
| Subject_Stats                   | Participant summary statistics    |
| Subject_Timepoint_Variable_Stat | Subject-by-timepoint summaries    |
| Subject_Missingness             | Participant missingness           |
| Subject_Timepoint_Stats         | Timepoint completeness            |
| Missing_By_Variable             | Variable missingness              |
| Missing_By_Timepoint            | Timepoint missingness             |
| Missing_By_Participant          | Participant missingness           |
| Missing_By_Part_Time            | Participant-timepoint missingness |
| Units_Audit                     | Unit verification                 |
| Naming_Audit                    | Variable naming audit             |
| Participant_Audit               | Participant coverage audit        |
| Inter_Subject_Variability       | Inter-subject variability         |
| Baseline_ISV                    | Baseline variability              |
| Variable_Coverage               | Variable coverage assessment      |
| Long_File_Variable_Inventory    | Long-file inventory               |

Purpose:

* Data quality assessment
* Missingness evaluation
* Coverage assessment
* Cohort characterization
* Harmonization planning

---

# Overlap Framework

The overlap framework identifies biomarkers shared across:

* Inspiration4
* NHANES
* UTMB Bed Rest Campaign 1

The resulting overlap dataset serves as the foundation for all cross-dataset analyses.

---

# Overlap Variables

The harmonized overlap framework contains 18 variables.

## Directly Measured Variables

* Albumin
* Alkaline Phosphatase
* ALT
* AST
* Total Bilirubin
* BUN
* Calcium
* Carbon Dioxide
* Chloride
* Creatinine
* CRP
* Glucose
* Potassium
* Total Protein
* Sodium

Total directly measured variables:

15

---

## Derived Variables

### Globulin

Derived as:

```text
Globulin = Total Protein − Albumin
```

---

### Albumin/Globulin Ratio

Derived as:

```text
Albumin / Globulin
```

---

### BUN/Creatinine Ratio

Derived as:

```text
BUN / Creatinine
```

---

Total overlap variables:

18

---

# Overlap Workbook

## LUNAR_Inspiration4_OVERLAP_Summary_v1.xlsx

Generated from:

```text
Inspiration4_Master_Long.csv
Inspiration4_Master_Wide.csv
```

Workbook contents:

| Worksheet                   | Description                           |
| --------------------------- | ------------------------------------- |
| Overlap_Crosswalk           | Harmonized variable mappings          |
| Derived_Variables_Audit     | Derived variable definitions          |
| Overlap_Data                | Participant-level overlap dataset     |
| Variable_Stats              | Overlap variable statistics           |
| Variable_Stats_By_Timepoint | Timepoint-specific overlap statistics |
| Subject_Stats               | Subject-level overlap summaries       |

Purpose:

* Cross-cohort harmonization
* NHANES comparison
* Bed Rest comparison
* Statistical analysis
* Mahalanobis analysis

---

# Timepoint Binning Framework

Different cohorts use different sampling schedules.

To facilitate direct comparison between astronaut, analog, and terrestrial datasets, three longitudinal binning strategies were developed.

Generated using:

```text
generate_inspiration4_timepoint_binning.py
```

Output:

```text
Inspiration4_Timepoint_Binning_Workbook_All3_Summaries.xlsx
```

---

## Option 1: Mean Preflight vs Mean Postflight

Preflight:

* Mean(L-92, L-44, L-3)

Postflight:

* Mean(R+1, R+45, R+82, R+194)

Purpose:

* Primary harmonization framework
* Noise reduction
* Cross-cohort comparison

---

## Option 2: Acute Response

Baseline:

* L-3

Postflight:

* R+1

Purpose:

* Immediate physiological response assessment
* Acute-response comparison

---

## Option 3: Long-Term Recovery

Preflight:

* Mean(L-92, L-44, L-3)

Recovery:

* Mean(R+45, R+82, R+194)

Purpose:

* Long-term recovery assessment
* Excludes acute R+1 effects

---

# Relationship to the Final LUNAR Analytical Panel

The overlap framework contains 18 variables.

CRP is retained within the overlap workbook because it is biologically relevant and available within Inspiration4 and Bed Rest datasets.

However, the final cross-dataset statistical and multivariate analyses use a locked 17-variable analytical panel.

CRP is excluded from:

* NHANES-referenced z-score analyses
* Final cross-dataset statistical analyses
* Repeated-measures analyses
* Whole-reference Mahalanobis calculations
* Bootstrap Mahalanobis sensitivity analyses

Final analytical panel:

* Albumin
* Albumin/Globulin Ratio
* Alkaline Phosphatase
* ALT
* AST
* Total Bilirubin
* BUN
* BUN/Creatinine Ratio
* Calcium
* Carbon Dioxide
* Chloride
* Creatinine
* Globulin
* Glucose
* Potassium
* Total Protein
* Sodium

---

# Relationship to Cross-Dataset Analyses

The Inspiration4 overlap dataset is integrated with:

```text
LUNAR_NHANES_OVERLAP_Summary_v2.xlsx
```

and

```text
LUNAR_BedRest_Campaign1_OVERLAP_Summary_v3.xlsx
```

to generate:

```text
LUNAR_Final18_Statistical_Comparison_Workbook.xlsx
```

This workflow supports:

* NHANES-referenced z-score calculations
* Cross-dataset statistical comparisons
* Repeated-measures ANOVA
* False-discovery-rate correction

---

# Relationship to Mahalanobis Analyses

The final 17-variable analytical panel is also used for:

## Whole-Reference Analysis

Output:

```text
LUNAR_Mahalanobis_Full_NHANES_Reference.xlsx
```

Purpose:

* Calculate global physiological distance from the NHANES reference population.

---

## Bootstrap Sensitivity Analysis

Output:

```text
mahalanobis_distance_summary.xlsx
```

Purpose:

* Evaluate sensitivity of Mahalanobis distances to NHANES sampling variability.

---

# Recommended Use

## Longitudinal Data Exploration

Use:

```text
Inspiration4_Master_Long.csv
```

for:

* Participant-level trajectories
* Timepoint exploration
* Biomarker visualization

---

## Data Integration

Use:

```text
Inspiration4_Master_Wide.csv
```

for:

* Harmonization
* Dataset integration
* Statistical analyses

---

## Quality Assessment

Use:

```text
Inspiration4_Data_Quality_Summary_v2_SubjectStats.xlsx
```

for:

* Missingness assessment
* Cohort characterization
* Quality control

---

## Cross-Dataset Harmonization

Use:

```text
LUNAR_Inspiration4_OVERLAP_Summary_v1.xlsx
```

for:

* NHANES comparisons
* Bed Rest comparisons
* Overlap analyses

---

## Longitudinal Harmonization

Use:

```text
Inspiration4_Timepoint_Binning_Workbook_All3_Summaries.xlsx
```

for:

* Preflight-versus-postflight analyses
* Acute-response analyses
* Recovery analyses
* Cross-cohort harmonization

---

# Current Status

Version 4.0

Completed:

* Data integration pipeline
* Demographic integration
* Long-format dataset generation
* Wide-format dataset generation
* Data-quality reporting
* Overlap harmonization
* Derived variable generation
* Longitudinal binning framework
* Cohort summary statistics
* NHANES harmonization
* Bed Rest harmonization
* NHANES-referenced statistical framework
* Mahalanobis analysis framework

Current outputs:

* Inspiration4_Master_Long.csv
* Inspiration4_Master_Wide.csv
* Inspiration4_Data_Quality_Summary_v2_SubjectStats.xlsx
* LUNAR_Inspiration4_OVERLAP_Summary_v1.xlsx
* Inspiration4_Timepoint_Binning_Workbook_All3_Summaries.xlsx

Status:

* Data integration complete
* Harmonization complete
* Quality-control reporting complete
* Longitudinal framework complete
* Cross-dataset framework complete
* Integrated into the LUNAR analytical framework

