# UTMB Bed Rest Campaign 1 Dataset for LUNAR

## Overview

This folder contains the UTMB Bed Rest Campaign 1 biomedical dataset, harmonization products, overlap datasets, longitudinal summaries, and quality-control reports generated as part of the LUNAR (Longitudinal Unification of Small-N Astronaut Responses) project.

The UTMB Bed Rest Campaign 1 dataset serves as the primary spaceflight analog cohort integrated into the LUNAR framework and is used for comparison against:

* NHANES terrestrial reference populations
* Inspiration4 commercial astronaut cohort
* Future astronaut and biomedical datasets incorporated into LUNAR

The purpose of this workflow is to create harmonized, analysis-ready datasets that support longitudinal physiological analyses and cross-cohort comparisons.

---

# Purpose

The Bed Rest workflow was designed to:

1. Harmonize participant-level bed rest data.
2. Standardize variable names and units.
3. Generate quality-control and completeness reports.
4. Identify biomarkers shared with Inspiration4 and NHANES.
5. Create derived variables required for overlap harmonization.
6. Generate longitudinal summary statistics.
7. Support NHANES-referenced z-score analyses.
8. Support Mahalanobis distance calculations within the LUNAR framework.

---

# Cohort Summary

Study:

* UTMB Bed Rest Campaign 1

Participants:

* C1G0001
* C1G0002
* C1G0003

Total Participants:

* 3

Primary Study Phases:

* PRE_TEST
* IN_TEST
* POST_TEST

Data Domains:

* Clinical chemistry
* Metabolic biomarkers
* Renal biomarkers
* Electrolytes
* Liver function biomarkers
* Inflammatory biomarkers

---

# Main Outputs

## Campaign1_Master_Long_REAL.xlsx

Primary harmonized Bed Rest dataset.

Characteristics:

* Long-format structure
* One row per observation
* Preserves participant-level longitudinal information
* Serves as the source dataset for all downstream analyses

Workbook contents:

| Worksheet   | Description                          |
| ----------- | ------------------------------------ |
| Master_Long | Harmonized participant-level dataset |

---

# Data Harmonization Workflow

The Bed Rest harmonization workflow standardizes variables and creates overlap-compatible datasets.

Processing steps:

1. Load participant-level Bed Rest laboratory data.
2. Standardize biomarker names.
3. Standardize participant identifiers.
4. Harmonize study phases.
5. Audit variable availability.
6. Generate overlap-compatible variables.
7. Generate quality-control reports.
8. Create overlap datasets for cross-cohort analyses.

---

# Data Quality Assessment

## Campaign1_Data_Quality_Summary_REAL.xlsx

Comprehensive quality-control and cohort characterization workbook.

Workbook contents:

| Worksheet                 | Description                   |
| ------------------------- | ----------------------------- |
| Dataset_Inventory         | Dataset overview              |
| Subject_Overview          | Participant inventory         |
| Variable_Stats            | Variable-level statistics     |
| Longitudinal_Summary      | Longitudinal coverage summary |
| Missing_By_Variable       | Variable missingness          |
| Missing_By_Participant    | Participant missingness       |
| Missing_By_Timepoint      | Phase missingness             |
| Units_Audit               | Unit verification             |
| Naming_Audit              | Variable naming audit         |
| Overlap_With_Inspiration4 | Overlap assessment            |

Purpose:

* Data quality assessment
* Missingness evaluation
* Coverage assessment
* Harmonization planning
* Cohort characterization

---

# Overlap Framework

The overlap framework identifies biomarkers shared across:

* UTMB Bed Rest Campaign 1
* Inspiration4
* NHANES

The overlap dataset serves as the foundation for all downstream cross-dataset analyses.

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

Three variables were derived to ensure direct comparability with Inspiration4 and NHANES.

### Globulin

Derived as:

Globulin = Total Protein − Albumin

---

### Albumin/Globulin Ratio

Derived as:

Albumin / Globulin

---

### BUN/Creatinine Ratio

Derived as:

BUN / Creatinine

---

Total overlap variables:

18

---

# Overlap Workbook

## LUNAR_BedRest_Campaign1_OVERLAP_Summary_v3.xlsx

This workbook contains the harmonized overlap dataset and supporting documentation.

Workbook contents:

| Worksheet                   | Description                         |
| --------------------------- | ----------------------------------- |
| Overlap_Crosswalk           | Harmonized variable mappings        |
| Derived_Variables_Audit     | Derived variable definitions        |
| Overlap_Data                | Participant-level overlap dataset   |
| Variable_Stats              | Overlap variable statistics         |
| Variable_Stats_By_Timepoint | Phase-specific overlap statistics   |
| Subject_Stats               | Participant-level overlap summaries |

Purpose:

* Cross-cohort harmonization
* NHANES comparison
* Inspiration4 comparison
* Statistical analysis
* Mahalanobis analysis

---

# Longitudinal Summary Workbook

## BedRest_Timepoint_Binning_Workbook.xlsx

This workbook summarizes participant-level and cohort-level longitudinal changes.

Each overlap biomarker receives an individual worksheet containing:

### Raw Participant Data

Participant-level measurements organized by:

* PRE_TEST
* IN_TEST
* POST_TEST

---

### Cohort Summary Statistics

For each biomarker:

* Pre mean
* Pre SD
* In mean
* In SD
* Post mean
* Post SD
* Delta calculations
* Percent change calculations

Purpose:

* Longitudinal characterization
* Phase-specific analysis
* Cross-cohort harmonization
* Statistical reporting

---

# Relationship to the Final LUNAR Analytical Panel

The overlap framework contains 18 variables.

CRP is retained within the overlap dataset because it is available in Bed Rest and Inspiration4 and is biologically relevant.

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

The Bed Rest overlap dataset is integrated with:

* LUNAR_NHANES_OVERLAP_Summary_v2.xlsx
* LUNAR_Inspiration4_OVERLAP_Summary_v1.xlsx

to generate:

LUNAR_Final18_Statistical_Comparison_Workbook.xlsx

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

LUNAR_Mahalanobis_Full_NHANES_Reference.xlsx

Purpose:

* Quantify global physiological deviation from the NHANES reference population.

---

## Bootstrap Sensitivity Analysis

Output:

mahalanobis_distance_summary.xlsx

Purpose:

* Evaluate sensitivity of Mahalanobis distances to sampling variability within the NHANES reference population.

---

# Recommended Use

## Data Exploration

Use:

Campaign1_Master_Long_REAL.xlsx

for:

* Participant-level review
* Longitudinal trajectory assessment
* Variable availability checks

---

## Data Quality Assessment

Use:

Campaign1_Data_Quality_Summary_REAL.xlsx

for:

* Missingness assessment
* Quality control
* Coverage evaluation
* Harmonization planning

---

## Cross-Dataset Harmonization

Use:

LUNAR_BedRest_Campaign1_OVERLAP_Summary_v3.xlsx

for:

* NHANES comparisons
* Inspiration4 comparisons
* Overlap assessments
* Statistical analyses
* Mahalanobis analyses

---

## Longitudinal Analysis

Use:

BedRest_Timepoint_Binning_Workbook.xlsx

for:

* Phase comparisons
* Longitudinal summaries
* Cohort-level reporting
* Cross-cohort harmonization

---

# Current Status

Version 3.0

Completed:

* Dataset harmonization
* Variable standardization
* Quality-control reporting
* Overlap framework development
* Derived variable generation
* Longitudinal summary framework
* NHANES harmonization
* Inspiration4 harmonization
* NHANES-referenced statistical framework
* Mahalanobis analysis framework

Current outputs:

* Campaign1_Master_Long_REAL.xlsx
* Campaign1_Data_Quality_Summary_REAL.xlsx
* LUNAR_BedRest_Campaign1_OVERLAP_Summary_v3.xlsx
* BedRest_Timepoint_Binning_Workbook.xlsx

Status:

* Harmonization complete
* Quality-control reporting complete
* Longitudinal framework complete
* Cross-dataset framework complete
* Integrated into the LUNAR analytical framework

