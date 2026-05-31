# project-lunar
# Inspiration4 Integrated Biomedical Dataset

## Overview

This repository contains scripts, derived datasets, and quality-control reports generated from Inspiration4 biomedical research data. The objective is to integrate multiple clinical chemistry, cytokine, immune, cardiovascular, and demographic datasets into standardized analysis-ready formats suitable for statistical analysis, machine learning, visualization, and longitudinal modeling.

The current release focuses on Inspiration4 serum biomarker, multiplex assay, clinical chemistry, and demographic data.

---

# Repository Structure

```text
Inspiration4_Project/
│
├── scripts/
│   ├── combine_inspiration4_data.py
│   └── summary_statistics.py
│
├── outputs/
│   ├── Inspiration4_Master_Long.csv
│   ├── Inspiration4_Master_Wide.csv
│   └── Inspiration4_Data_Quality_Summary.xlsx
│
├── README.md
│
└── requirements.txt
```

---

# Source Data

The integrated datasets were generated from the following Inspiration4 source files:

### Clinical Chemistry

* LSDS-8_Comprehensive_Metabolic_Panel_CMP.upload_SUBMITTED.csv

### Multiplex Biomarker Panels

* LSDS-8_Multiplex_serum.cardiovascular.EvePanel_SUBMITTED.csv
* LSDS-8_Multiplex_serum.immune.EvePanel_SUBMITTED.csv
* LSDS-8_Multiplex_serum.immune.AlamarPanel_SUBMITTED.xlsx

### Demographics

* Demographics_inspiration4.xlsx

These datasets contain measurements related to:

* Clinical chemistry
* Immune biomarkers
* Cytokines
* Cardiovascular biomarkers
* Demographics
* Longitudinal sampling across mission-relevant timepoints

---

# Data Integration Pipeline

## combine_inspiration4_data.py

This script:

1. Loads all source datasets.
2. Standardizes column names.
3. Harmonizes participant identifiers.
4. Harmonizes sampling timepoints.
5. Merges demographic information.
6. Combines biomarker panels into a unified structure.
7. Produces both long-format and wide-format datasets.

Run:

```bash
py scripts/combine_inspiration4_data.py
```

Generated outputs:

* Inspiration4_Master_Long.csv
* Inspiration4_Master_Wide.csv

---

# Data Quality Pipeline

## summary_statistics.py

This script performs automated quality-control and descriptive statistical analyses.

Generated summaries include:

* Dataset inventory
* Participant counts
* Timepoint counts
* Demographic summaries
* Variable-level descriptive statistics
* Missingness by variable
* Missingness by participant
* Missingness by timepoint
* Missingness by participant/timepoint
* Unit audits
* Variable naming audits

Run:

```bash
py scripts/summary_statistics.py
```

Generated output:

* Inspiration4_Data_Quality_Summary.xlsx

---

# Outputs

## Inspiration4_Master_Long.csv

Integrated long-format dataset.

Characteristics:

* One row per measurement
* Suitable for longitudinal analyses
* Suitable for mixed-effects models
* Suitable for repeated-measures statistics

Dimensions:

* 8,252 rows
* 14 columns

---

## Inspiration4_Master_Wide.csv

Integrated wide-format dataset.

Characteristics:

* One row per participant-timepoint
* Suitable for PCA
* Suitable for clustering
* Suitable for correlation analysis
* Suitable for machine learning workflows

Dimensions:

* 28 rows
* 304 columns

---

## Inspiration4_Data_Quality_Summary.xlsx

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

# Software Requirements

Python Version:

```text
Python 3.10+
```

Required packages:

```text
pandas
numpy
openpyxl
```

Install dependencies:

```bash
pip install pandas numpy openpyxl
```

---

# Dataset Version History

## v1.0 (2026-05-31)

Initial integrated Inspiration4 biomedical dataset.

Included:

* Comprehensive Metabolic Panel (CMP)
* Cardiovascular multiplex biomarkers
* Immune multiplex biomarkers
* Alamar immune biomarkers
* Demographic data
* Long-format integrated dataset
* Wide-format integrated dataset
* Automated data quality report

Generated outputs:

* Inspiration4_Master_Long.csv
* Inspiration4_Master_Wide.csv
* Inspiration4_Data_Quality_Summary.xlsx

---

# Planned Analyses

Future analyses may include:

* Principal Component Analysis (PCA)
* Longitudinal trajectory modeling
* Mixed-effects modeling
* Biomarker correlation networks
* Clustering and heatmaps
* Cytokine profiling
* Clinical chemistry trend analysis
* Cross-dataset integration with additional Inspiration4 and LSDA datasets

---

# Citation

If using this repository, please cite the original Inspiration4 data source, associated publications, and any downstream analyses generated from these integrated datasets.

---

# Disclaimer

This repository contains derived research datasets generated from publicly available Inspiration4 source data. Users are responsible for verifying analyses, validating results, and complying with all applicable data-use and citation requirements.

