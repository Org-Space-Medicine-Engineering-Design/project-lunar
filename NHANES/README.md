# NHANES Terrestrial Reference Dataset

## Overview

This folder contains NHANES (National Health and Nutrition Examination Survey) datasets curated for the LUNAR (Longitudinal Unification of Small-N Astronaut Responses) project.

The purpose of this dataset is to establish a terrestrial reference population that can be compared with astronaut cohorts and spaceflight analog populations. NHANES provides large-scale population-level measurements that serve as a baseline for interpreting physiological changes observed in small-N astronaut studies.

---

## Purpose within LUNAR

LUNAR aims to harmonize biomedical datasets across astronaut, analog, and terrestrial populations.

Within this framework, NHANES serves as:

* A terrestrial reference population
* A source of demographic baseline distributions
* A source of clinical chemistry reference values
* A source of anthropometric reference values
* A harmonization target for cross-cohort comparisons

Future analyses will compare NHANES participants with:

* Inspiration4 astronauts
* Bed rest analog cohorts
* Additional astronaut cohorts
* Future commercial and government spaceflight datasets

---

## Current Dataset

This folder contains the first NHANES working dataset focused on biochemical profile variables and cohort-filtering variables relevant to space medicine and astronaut health.

The goal of this first pull was to create a clean, merged terrestrial reference dataset suitable for future harmonization with astronaut and analog datasets.

---

## Main Files

### processed_csv/nhanes_biochemical_profile_first_pull.csv

Full merged first-pass dataset containing all merged NHANES source files.

---

### processed_csv/nhanes_biochemical_profile_first_pull_70pct_available.csv

Filtered dataset retaining:

* SEQN
* Variables with at least 70% availability

Purpose:

* Initial exploratory analyses
* Reduced missingness workflows

---

### processed_csv/nhanes_biochemical_model_ready_keep_columns.csv

Model-ready dataset containing variables designated:

* Keep

based on the completed variable mapping process.

---

### processed_csv/nhanes_biochemical_model_ready_keep_support_columns.csv

Model-ready dataset containing variables designated:

* Keep
* Support

This is the recommended dataset for first-pass exploratory analyses and harmonization efforts.

---

## Summary Files

### summaries/nhanes_first_pull_column_map_completed.csv

Completed variable map including:

* Variable descriptions
* Measure groups
* LUNAR relevance
* Keep / Support / Review decisions

---

### summaries/nhanes_model_ready_group_summary.csv

Summary of retained variables by measure group.

---

### summaries/nhanes_model_ready_missingness_summary.csv

Missingness assessment for the model-ready dataset.

---

### summaries/nhanes_model_ready_numeric_summary.csv

Descriptive statistics for retained numeric variables.

---

## Source Files Used

The current first-pass merge includes 14 NHANES public-use datasets:

### Demographics

* P_DEMO

### Anthropometrics

* P_BMX

### Blood Pressure

* P_BPXO

### Hematology

* P_CBC

### Exposure Biomarkers

* P_COT

### Kidney Function

* P_ALB_CR

### Lipids

* P_HDL
* P_TCHOL
* P_TRIGLY

### Dietary Intake

* P_DR1TOT
* P_DR2TOT

### Dietary Supplements

* P_DS1TOT
* P_DS2TOT
* P_DSQTOT

---

## Merge Strategy

All source datasets were merged using:

```text
SEQN
```

the unique NHANES participant identifier.

---

## Cohort Summary

Current merged dataset:

* 15,560 unique participants
* No duplicate SEQN values

Population type:

* General U.S. population

Role within LUNAR:

* Terrestrial comparison cohort

---

## Recommended Files

### For Exploratory Analysis

Use:

```text
processed_csv/
nhanes_biochemical_model_ready_keep_support_columns.csv
```

Recommended analyses:

* PCA
* Clustering
* Correlation analysis
* Variable harmonization

---

### For Missingness Evaluation

Use:

```text
summaries/
nhanes_model_ready_missingness_summary.csv
```

---

### For Variable Mapping

Use:

```text
summaries/
nhanes_first_pull_column_map_completed.csv
```

---

## Harmonization Goals

Future harmonization efforts will align NHANES variables with:

| Domain             | Example Variables               |
| ------------------ | ------------------------------- |
| Demographics       | Age, Sex, BMI                   |
| Anthropometrics    | Height, Weight                  |
| Clinical Chemistry | Glucose, Albumin, Creatinine    |
| Lipids             | HDL, Cholesterol, Triglycerides |
| Hematology         | CBC Measures                    |
| Nutrition          | Dietary Intake                  |
| Supplements        | Vitamin and Mineral Use         |
| Cardiovascular     | Blood Pressure                  |

These mappings will support direct comparison with astronaut and analog cohorts.

---

## Current Status

### Version 1.0

Completed:

* Initial NHANES dataset acquisition
* Dataset merging
* Variable mapping
* Missingness assessment
* Model-ready dataset generation

Current outputs:

* Merged NHANES dataset
* Filtered NHANES dataset
* Model-ready datasets
* Missingness summaries
* Variable mapping tables

Status:

* Ready for harmonization with astronaut and analog cohorts

---

## Relationship to LUNAR

NHANES serves as the primary terrestrial reference population within the LUNAR framework.

By comparing astronaut cohorts against large terrestrial populations, LUNAR seeks to determine whether observed physiological responses represent:

* Normal population variation
* Spaceflight-associated adaptation
* Analog-associated adaptation
* Unique astronaut physiological signatures

---

## Citation

Please cite the National Health and Nutrition Examination Survey (NHANES) and associated documentation when using these datasets or derived products.

---

## Disclaimer

This folder contains derived datasets generated from publicly available NHANES data. Users are responsible for verifying analyses, validating results, and complying with all applicable NHANES data-use and citation requirements.

