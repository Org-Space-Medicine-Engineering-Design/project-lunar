# Inspiration4 Biomedical Dataset

## Overview

This folder contains the Inspiration4 cohort datasets, processing scripts, derived datasets, and quality-control reports generated as part of the LUNAR (Longitudinal Unification of Small-N Astronaut Responses) project.

The purpose of this dataset is to create analysis-ready longitudinal biomedical data products from the Inspiration4 mission that can be compared with terrestrial reference populations (e.g., NHANES) and spaceflight analog cohorts (e.g., bed rest studies).

---

## Source Data

The integrated datasets were generated from the following Inspiration4 source files:

### Clinical Chemistry

* LSDS-8_Comprehensive_Metabolic_Panel_CMP.upload_SUBMITTED.csv

### Multiplex Biomarker Panels

* LSDS-8_Multiplex_serum.cardiovascular.EvePanel_SUBMITTED.csv
* LSDS-8_Multiplex_serum.immune.EvePanel_SUBMITTED.csv
* LSDS-8_Multiplex_serum.immune.AlamarPanel_SUBMITTED.xlsx

### Demographics

* Demographics_inspiration4.xlsx

These datasets include:

* Clinical chemistry measurements
* Immune biomarkers
* Cytokines
* Cardiovascular biomarkers
* Demographic information
* Longitudinal sampling timepoints

---

## Processing Pipeline

### combine_inspiration4_data.py

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

### summary_statistics_inspiration4_v2.py

This script generates the Inspiration4 quality-control and summary workbook from the integrated master datasets rather than directly from the raw assay files.

Inputs:

* Inspiration4_Master_Wide.csv
* Inspiration4_Master_Long.csv
* Demographics_inspiration4.xlsx

The script reconstructs a longitudinal data structure from the master datasets and produces a LUNAR-compatible quality-control workbook aligned with the Bed Rest Campaign 1 summary framework.

Key features include:

* Dataset inventory and cohort summary
* Demographic integration
* Variable-level summary statistics
* Variable-level summary statistics by timepoint
* Variable-level missingness assessments
* Subject-level summary statistics
* Subject-level missingness assessments
* Subject × timepoint coverage assessments
* Participant audit tables
* Inter-subject variability analysis
* Baseline inter-subject variability analysis
* Variable coverage metrics
* Units audit
* Variable naming audit

Run:

```bash
py scripts/summary_statistics_inspiration4_v2.py
```

Output:

* Inspiration4_Data_Quality_Summary_V2.xlsx

The summary workbook is generated exclusively from the integrated master datasets and does not include raw source-file observation tables.

---

## Available Outputs

### Inspiration4_Master_Long.csv

Integrated long-format dataset.

Characteristics:

* One row per measurement
* Preserves longitudinal structure
* Suitable for mixed-effects models
* Suitable for repeated-measures analyses
* Suitable for longitudinal visualization

Current dimensions:

* 8,252 rows
* 14 columns

---

### Inspiration4_Master_Wide.csv

Integrated wide-format dataset.

Characteristics:

* One row per participant-timepoint
* Suitable for PCA
* Suitable for clustering
* Suitable for correlation analysis
* Suitable for machine learning workflows

Current dimensions:

* 28 rows
* 304 columns

---

### Inspiration4_Data_Quality_Summary_V2.xlsx

Comprehensive quality-control and cohort summary workbook.

Workbook tabs include:

* Dataset_Inventory
* Demographics
* Variable_Stats
* Variable_Stats_By_Timepoint
* Subject_Stats
* Subject_Missingness
* Subject_Timepoint_Stats
* Missing_By_Variable
* Missing_By_Timepoint
* Units_Audit
* Naming_Audit
* Participant_Audit
* Inter_Subject_Variability
* Baseline_ISV
* Variable_Coverage

Characteristics:

* Generated from integrated master datasets
* No raw source-file observation tables included
* Aligned with the Bed Rest Campaign 1 summary structure
* Designed for rapid quality control, cohort characterization, and cross-cohort harmonization within the LUNAR framework

---

## Cohort Summary

Mission:

* Inspiration4

Cohort Size:

* 4 participants

Longitudinal Sampling Timepoints:

* L-92
* L-44
* L-3
* FD2
* FD3
* R+1
* R+45
* R+82

Data Domains:

* Demographics
* Clinical chemistry
* Immune biomarkers
* Cytokines
* Cardiovascular biomarkers
* Inflammatory biomarkers

Approximate Variables:

* 299 unique biomarker variables
* 304 total feature columns in the integrated wide-format dataset

---

## Recommended Files

### For Longitudinal Statistical Modeling

Use:

* Inspiration4_Master_Long.csv

Recommended methods:

* Mixed-effects models
* Repeated-measures ANOVA
* Longitudinal trajectory analysis
* Generalized estimating equations

---

### For Multivariate Analysis

Use:

* Inspiration4_Master_Wide.csv

Recommended methods:

* Principal Component Analysis (PCA)
* UMAP
* Hierarchical clustering
* Correlation networks
* Machine learning workflows

---

### For Data Exploration and Quality Assessment

Use:

* Inspiration4_Data_Quality_Summary_V2.xlsx

Recommended uses:

* Missingness assessment
* Cohort characterization
* Participant-level quality control
* Variable-level quality control
* Baseline variability assessment
* Cross-cohort harmonization planning

---

## Relationship to Bed Rest Harmonization

The Inspiration4 quality-control workbook was intentionally structured to mirror the Bed Rest Campaign 1 overlap summary workbook.

Shared reporting elements include:

* Dataset inventory
* Variable summary statistics
* Variable-level missingness
* Subject-level summary statistics
* Subject-level missingness
* Participant audit tables
* Units audit
* Coverage assessment

This standardized reporting framework facilitates direct comparison between:

* Inspiration4
* Bed Rest Campaign 1
* NHANES

and future cohorts incorporated into the LUNAR project.

---

## Current Status

### Version 2.0

Completed:

* Data integration pipeline
* Demographic integration
* Long-format dataset generation
* Wide-format dataset generation
* Inspiration4 quality-control framework
* Subject-level quality-control reporting
* Inter-subject variability analysis
* Baseline variability assessment
* LUNAR-compatible summary workbook generation

Current outputs:

* Inspiration4_Master_Long.csv
* Inspiration4_Master_Wide.csv
* Inspiration4_Data_Quality_Summary_V2.xlsx

Status:

* Analysis-ready
* Harmonized for comparison with Bed Rest Campaign 1
* Prepared for NHANES integration within the LUNAR framework

---

## Planned Analyses

Planned analyses include:

* Principal Component Analysis (PCA)
* Longitudinal trajectory modeling
* Biomarker correlation networks
* Immune profiling
* Clinical chemistry trend analysis
* Comparison with NHANES terrestrial reference populations
* Comparison with bed rest analog cohorts
* Cross-cohort harmonization within the LUNAR framework
* Development of common biomarker panels across astronaut, analog, and terrestrial populations

---

## Relationship to LUNAR

This dataset represents the first integrated astronaut cohort within the LUNAR project.

Future LUNAR analyses will compare Inspiration4 biomarker profiles with:

* NHANES terrestrial reference populations
* Bed Rest Campaign 1
* Additional bed rest campaigns
* Additional astronaut cohorts
* Future commercial spaceflight datasets

The long-term objective is to identify common and cohort-specific physiological responses associated with spaceflight, analog environments, and operationally relevant human performance stressors.

---

## Citation

If using this dataset or derived products, please cite:

* The original Inspiration4 data source
* Associated Inspiration4 publications
* NASA Open Science Data Repository (OSDR) records where applicable
* Any downstream analyses generated from these integrated datasets

---

## Disclaimer

This folder contains derived datasets generated from publicly available Inspiration4 source data.

Users are responsible for:

* Verifying analyses
* Validating results
* Confirming variable harmonization
* Maintaining reproducible workflows
* Complying with all applicable data-use agreements and citation requirements

Derived datasets and summary products are intended to facilitate reproducible analysis within the LUNAR framework and do not replace the original source datasets.

