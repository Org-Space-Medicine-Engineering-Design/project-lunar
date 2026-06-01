# project-lunar
# LUNAR: Longitudinal Unification of Small-N Astronaut Responses

## Overview

LUNAR (Longitudinal Unification of Small-N Astronaut Responses) is a data harmonization and analytics project focused on integrating astronaut, astronaut-relevant, analog, and terrestrial biomedical datasets into a common framework for cross-cohort comparison.

A major challenge in space medicine is the limited sample size available within astronaut populations. Individual studies often contain only a small number of participants, making it difficult to distinguish mission-specific findings from broader physiological trends. LUNAR addresses this challenge by creating standardized, analysis-ready datasets that enable comparison across multiple independent cohorts.

The project aims to support future investigations into physiological adaptation, recovery, resilience, and health risks associated with spaceflight and spaceflight-relevant environments.

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

Ground-based physiological analog studies.

Planned datasets include:

* DLR Envihab
* NASA Bed Rest Studies
* Additional publicly available analog cohorts

Purpose within LUNAR:

* Spaceflight analog comparisons
* Physiological deconditioning analyses
* Isolation and confinement comparisons

Current status:

* Data acquisition and harmonization in progress

---

## Repository Structure

```text
LUNAR/
│
├── README.md
│
├── Inspiration4/
│   ├── README.md
│   ├── scripts/
│   ├── outputs/
│   └── data/
│
├── NHANES/
│   ├── README.md
│   ├── processed_csv/
│   ├── summaries/
│   └── scripts/
│
├── BedRest/
│   ├── README.md
│   └── data/
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

* Inspiration4 integration pipeline
* Inspiration4 quality-control reporting pipeline
* Initial NHANES harmonization effort
* NHANES missingness and descriptive statistics reporting

In Progress:

* Variable mapping across cohorts
* Common data dictionary development
* Bed rest dataset integration

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

## Long-Term Vision

The long-term goal of LUNAR is to establish a unified framework for evaluating longitudinal physiological responses across astronaut, analog, and terrestrial populations.

By integrating multiple small-N astronaut cohorts with large terrestrial reference populations and ground-based analog studies, LUNAR aims to improve interpretation of astronaut biomedical data and support future evidence-based space medicine research.

---

## Contributors

LUNAR is a collaborative effort focused on developing harmonized biomedical datasets and analytical tools for space medicine research.

---

## Citation

If using datasets, scripts, or derived products from this repository, please cite the original source datasets and associated publications where appropriate.

---

## Disclaimer

This repository contains derived datasets generated from publicly available and/or collaborator-provided source data. Users are responsible for verifying analyses, validating results, and complying with all applicable data-use agreements and citation requirements.
