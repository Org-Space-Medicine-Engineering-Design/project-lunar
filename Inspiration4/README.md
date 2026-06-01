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
6. Combines biomarker panels into a unified structure.
7. Generates long-format and wide-format datasets.

Run:

```bash
py scripts/combine_inspiration4_data.py
```

Outputs:

* Inspiration4_Master_Long.csv
* Inspiration4_Master_Wide.csv

---

### summary_statistics.py

This script generates an automated data-quality report.

Outputs include:

* Dataset inventory
* Participant counts
* Timepoint counts
* Demographic summaries
* Variable summary statistics
* Missingness assessments
* Units audit
* Variable naming audit

Run:

```bash
py scripts/summary_statistics.py
```

Output:

* Inspiration4_Data_Quality_Summary.xlsx

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

### Inspiration4_Data_Quality_Summary.xlsx

Automated quality-control workbook.

Workbook tabs include:

* Dataset_Inventory
* Demographics
* Variable_Stats
* Missing_By_Variable
* Missing_By_Participant
* Missing_By_Timepoint
* Missing_By_Part_Time
* Units_Audit
* Naming_Audit

---

## Cohort Summary

Mission:

* Inspiration4

Cohort Size:

* 4 participants

Longitudinal Sampling:

* Multiple pre-flight and post-flight collection timepoints

Data Domains:

* Demographics
* Clinical chemistry
* Immune biomarkers
* Cardiovascular biomarkers

---

## Recommended Files

### For Longitudinal Statistical Modeling

Use:

* Inspiration4_Master_Long.csv

Recommended methods:

* Mixed-effects models
* Repeated-measures ANOVA
* Longitudinal trajectory analysis

---

### For Multivariate Analysis

Use:

* Inspiration4_Master_Wide.csv

Recommended methods:

* PCA
* UMAP
* Clustering
* Correlation networks
* Machine learning

---

### For Data Exploration and Quality Assessment

Use:

* Inspiration4_Data_Quality_Summary.xlsx

---

## Current Status

### Version 1.0

Completed:

* Data integration pipeline
* Demographic integration
* Long-format dataset generation
* Wide-format dataset generation
* Automated data-quality reporting

Current outputs:

* Inspiration4_Master_Long.csv
* Inspiration4_Master_Wide.csv
* Inspiration4_Data_Quality_Summary.xlsx

Status:

* Analysis-ready

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

---

## Relationship to LUNAR

This dataset represents the first integrated astronaut cohort within the LUNAR project.

Future LUNAR analyses will compare Inspiration4 biomarker profiles with:

* NHANES terrestrial reference populations
* Bed rest analog cohorts
* Additional astronaut cohorts
* Future commercial spaceflight datasets

The long-term objective is to identify common and cohort-specific physiological responses associated with spaceflight and related operational environments.

---

## Citation

If using this dataset or derived products, please cite the original Inspiration4 data source, associated publications, and any downstream analyses generated from these integrated datasets.

---

## Disclaimer

This folder contains derived datasets generated from publicly available Inspiration4 source data. Users are responsible for verifying analyses, validating results, and complying with all applicable data-use agreements and citation requirements.

