# project-lunar
# LUNAR: Longitudinal Unification of Small-N Astronaut Responses

## Overview

LUNAR (Longitudinal Unification of Small-N Astronaut Responses) is a data harmonization and analytics project focused on integrating astronaut, astronaut-relevant, analog, and terrestrial biomedical datasets into a common framework for cross-cohort comparison.

A major challenge in space medicine is the limited sample size available within astronaut populations. Individual studies often contain only a small number of participants, making it difficult to distinguish mission-specific findings from broader physiological trends. LUNAR addresses this challenge by creating standardized, analysis-ready datasets that enable comparison across multiple independent cohorts.

The project is designed to support future investigations into physiological adaptation, recovery, resilience, and health risks associated with spaceflight and spaceflight-relevant environments.

---

## Mission

The mission of LUNAR is to create a unified framework for comparing longitudinal physiological responses across:

* Commercial astronaut cohorts
* Government astronaut cohorts
* Ground-based analog cohorts
* Terrestrial reference populations

By harmonizing data across these groups, LUNAR seeks to identify both common and cohort-specific physiological responses associated with spaceflight and related operational environments.

---

## Current Cohorts

### Inspiration4

Commercial astronaut mission dataset.

Current data domains include:

* Comprehensive Metabolic Panel (CMP)
* Immune biomarkers
* Cardiovascular biomarkers
* Multiplex cytokine panels
* Demographics

Purpose within LUNAR:

* Commercial astronaut reference cohort
* Longitudinal spaceflight response characterization

Current status:

* Integrated
* Quality controlled
* Analysis-ready

Available outputs:

* Inspiration4_Master_Long.csv
* Inspiration4_Master_Wide.csv
* Inspiration4_Data_Quality_Summary.xlsx

---

### NHANES

National Health and Nutrition Examination Survey (NHANES).

Current data domains include:

* Demographics
* Anthropometrics
* Blood pressure
* Clinical chemistry
* Hematology
* Lipid profiles
* Dietary intake
* Supplement use
* Exposure biomarkers

Purpose within LUNAR:

* Terrestrial reference population
* Population-level baseline comparison cohort

Current status:

* Initial harmonization complete
* Model-ready datasets generated

---

### Bed Rest Cohorts

Ground-based physiological analog studies designed to simulate selected effects of spaceflight and physiological deconditioning.

Current efforts focus on harmonizing biomedical datasets derived from bed rest campaigns curated through the University of Texas Medical Branch (UTMB).

Potential data domains include:

* Clinical chemistry
* Hematology
* Immune biomarkers
* Cardiovascular measures
* Anthropometrics
* Physiological monitoring
* Nutrition-related variables

Purpose within LUNAR:

* Spaceflight analog comparisons
* Physiological deconditioning analyses
* Longitudinal adaptation and recovery studies
* Evaluation of analog-to-spaceflight similarities and differences

Current status:

* Data acquisition and harmonization in progress
* Variable mapping and cohort characterization underway

---

## Repository Structure

```text
LUNAR/
│
├── README.md
│
├── Inspiration4/
│   ├── README.md
│   ├── data/
│   ├── outputs/
│   └── scripts/
│
├── NHANES/
│   ├── README.md
│   ├── data/
│   ├── outputs/
│   └── scripts/
│
├── BedRest/
│   ├── README.md
│   ├── data/
│   ├── outputs/
│   └── scripts/
│
├── Harmonization/
│
└── Documentation/
```

---

## Harmonization Strategy

LUNAR seeks to create a common variable framework across all participating cohorts.

Target harmonized domains include:

| Domain             | Example Variables                    |
| ------------------ | ------------------------------------ |
| Demographics       | Age, Sex, BMI                        |
| Anthropometrics    | Height, Weight                       |
| Clinical Chemistry | Glucose, Albumin, Creatinine         |
| Hematology         | CBC Measures                         |
| Lipids             | HDL, LDL, Cholesterol, Triglycerides |
| Inflammation       | Cytokines, CRP                       |
| Nutrition          | Dietary Intake                       |
| Supplements        | Vitamin and Mineral Use              |
| Cardiovascular     | Blood Pressure, Biomarkers           |

Future work will generate a common data dictionary enabling direct comparison across astronaut, analog, and terrestrial cohorts.

---

## Current Status

### Version 1.0

Completed:

* Inspiration4 data integration pipeline
* Inspiration4 quality-control reporting pipeline
* Initial NHANES harmonization effort
* NHANES missingness and descriptive statistics reporting

In Progress:

* Variable mapping across cohorts
* Common data dictionary development
* UTMB bed rest campaign integration

Planned:

* Cross-cohort comparison datasets
* Principal Component Analysis (PCA)
* UMAP and clustering analyses
* Longitudinal trajectory modeling
* Mixed-effects modeling
* Predictive modeling
* Biomarker harmonization

---

## Recommended Starting Points

### Inspiration4

Recommended files:

* Inspiration4_Master_Long.csv
* Inspiration4_Master_Wide.csv
* Inspiration4_Data_Quality_Summary.xlsx

See:

```text
Inspiration4/README.md
```

for details.

---

### NHANES

Recommended files:

* nhanes_biochemical_model_ready_keep_support_columns.csv
* nhanes_model_ready_numeric_summary.csv
* nhanes_model_ready_missingness_summary.csv

See:

```text
NHANES/README.md
```

for details.

---

### Bed Rest

Current datasets are undergoing harmonization and variable mapping.

Future outputs will include:

* Harmonized longitudinal datasets
* Missingness assessments
* Descriptive statistics summaries
* Cross-cohort variable mapping tables

See:

```text
BedRest/README.md
```

for updates.

---

## Long-Term Vision

The long-term goal of LUNAR is to establish a unified framework for evaluating longitudinal physiological responses across astronaut, analog, and terrestrial populations.

By integrating multiple small-N astronaut cohorts with large terrestrial reference populations and UTMB bed rest campaigns, LUNAR aims to improve interpretation of astronaut biomedical data and support future evidence-based space medicine research.

Ultimately, LUNAR will enable researchers to determine whether observed physiological changes represent:

* Normal population variation
* Spaceflight-associated adaptation
* Analog-associated adaptation
* Unique astronaut physiological signatures

---

## Contributors

LUNAR is a collaborative effort focused on developing harmonized biomedical datasets and analytical tools for space medicine research.

---

## Citation

If using datasets, scripts, or derived products from this repository, please cite the original source datasets and associated publications where appropriate.

---

## Disclaimer

This repository contains derived datasets generated from publicly available and/or collaborator-provided source data. Users are responsible for verifying analyses, validating results, and complying with all applicable data-use agreements and citation requirements.

