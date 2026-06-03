# Inspiration4 Biomedical Dataset

## Overview

This folder contains the Inspiration4 cohort datasets, processing scripts, derived datasets, and quality-control reports generated as part of the **LUNAR (Longitudinal Unification of Small-N Astronaut Responses)** project.

The purpose of this dataset is to create analysis-ready longitudinal biomedical data products from the Inspiration4 mission that can be compared with terrestrial reference populations (e.g., NHANES) and spaceflight analog cohorts (e.g., bed rest studies).

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
2. A Bed Rest–aligned overlap workbook containing only approved overlap variables.

Run:

```bash
py scripts/summary_statistics_inspiration4_v2.py \
    --wide outputs/Inspiration4_Master_Wide.csv \
    --long outputs/Inspiration4_Master_Long.csv \
    --demographics data/raw/Inspiration4/Demographics_inspiration4.xlsx \
    --out outputs/Inspiration4_Data_Quality_Summary_V2.xlsx \
    --overlap-out outputs/Inspiration4_BedRest_Overlap_Summary_v3_with_BUN.xlsx
```

Outputs:

* Inspiration4_Data_Quality_Summary_V2.xlsx
* Inspiration4_BedRest_Overlap_Summary_v3_with_BUN.xlsx

The full summary workbook is generated exclusively from the harmonized master datasets and does not include raw source-file observation tables.

The overlap workbook is generated using a locked Inspiration4-to-Bed Rest crosswalk and is intended for direct comparison with Bed Rest Campaign 1 and future harmonized datasets.

---

# Available Outputs

## Inspiration4_Master_Long.csv

Integrated long-format dataset.

Characteristics:

* One row per measurement
* Preserves longitudinal structure
* Suitable for mixed-effects models
* Suitable for repeated-measures analyses
* Suitable for longitudinal visualization

---

## Inspiration4_Master_Wide.csv

Integrated wide-format dataset.

Characteristics:

* One row per participant-timepoint
* Suitable for PCA
* Suitable for clustering
* Suitable for correlation analysis
* Suitable for machine-learning workflows

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
* No raw source-file observation tables included
* Aligned with the Bed Rest reporting framework
* Designed for rapid quality control, cohort characterization, and cross-cohort harmonization

---

## Inspiration4_BedRest_Overlap_Summary_v3_with_BUN.xlsx

Bed Rest–aligned overlap summary workbook containing only approved overlap variables shared between Inspiration4 and Bed Rest Campaign 1.

This workbook is generated using a locked crosswalk and does not rely on fuzzy variable matching.

### Included Canonical Variables

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

### Locked Crosswalk

| Canonical Variable     | Inspiration4 Source Column  |
| ---------------------- | --------------------------- |
| ALBUMIN                | CMP__ALBUMIN                |
| ALKALINE PHOSPHATASE   | CMP__ALKALINE PHOSPHATASE   |
| ALT                    | CMP__ALT                    |
| AST                    | CMP__AST                    |
| BILIRUBIN; TOTAL       | CMP__BILIRUBIN; TOTAL       |
| CALCIUM                | CMP__CALCIUM                |
| CARBON DIOXIDE         | CMP__CARBON DIOXIDE         |
| CHLORIDE               | CMP__CHLORIDE               |
| CREATININE             | CMP__CREATININE             |
| CRP                    | Cardiovascular_Eve__CRP     |
| GLUCOSE                | CMP__GLUCOSE                |
| POTASSIUM              | CMP__POTASSIUM              |
| PROTEIN; TOTAL         | CMP__PROTEIN; TOTAL         |
| SODIUM                 | CMP__SODIUM                 |
| BUN                    | CMP__UREA NITROGEN (BUN)    |
| UREA NITROGEN (BUN)    | CMP__UREA NITROGEN (BUN)    |
| GLOBULIN               | CMP__GLOBULIN               |
| ALBUMIN/GLOBULIN RATIO | CMP__ALBUMIN/GLOBULIN RATIO |
| BUN/CREATININE RATIO   | CMP__BUN/CREATININE RATIO   |

### Workbook Tabs

* Dataset_Inventory
* Variable_Stats
* Variable_Stats_By_Timepoint
* Subject_Stats
* Subject_Timepoint_Variable_Stat
* Subject_Missingness
* Subject_Timepoint_Stats
* Missing_By_Variable
* Missing_By_Timepoint
* Overlap_Crosswalk
* Units_Audit
* Derived_Variables_Audit
* Participant_Audit
* Overlap_Data

Characteristics:

* Generated from Inspiration4_Master_Wide.csv
* Uses a locked crosswalk to prevent accidental inclusion of similarly named biomarkers
* Mirrors the Bed Rest Campaign 1 overlap summary structure
* Includes participant-level, variable-level, and timepoint-level quality-control metrics
* Intended for direct comparison with Bed Rest and future harmonized datasets

---

# Cohort Summary

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

---

# Recommended Files

## For Longitudinal Statistical Modeling

Use:

* Inspiration4_Master_Long.csv

Recommended methods:

* Mixed-effects models
* Repeated-measures ANOVA
* Longitudinal trajectory analysis
* Generalized estimating equations

---

## For Multivariate Analysis

Use:

* Inspiration4_Master_Wide.csv

Recommended methods:

* Principal Component Analysis (PCA)
* UMAP
* Hierarchical clustering
* Correlation networks
* Machine learning workflows

---

## For Data Exploration and Quality Assessment

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

## For Bed Rest Harmonization

Use:

* Inspiration4_BedRest_Overlap_Summary_v3_with_BUN.xlsx

Recommended uses:

* Direct astronaut-versus-bed-rest comparison
* Harmonized biomarker assessment
* Shared-variable analyses
* Cross-cohort effect size estimation
* Preparation for future NHANES overlap analyses

---

# Relationship to Bed Rest Harmonization

The Inspiration4 overlap workbook was intentionally structured to mirror the Bed Rest Campaign 1 overlap workbook.

Shared reporting elements include:

* Dataset inventory
* Variable summary statistics
* Variable-level missingness
* Subject-level summary statistics
* Subject-level missingness
* Participant audit tables
* Units audit
* Coverage assessment

This standardized framework facilitates direct comparison between:

* Inspiration4
* Bed Rest Campaign 1
* Future Bed Rest Campaigns
* NHANES (future harmonization)

---

# Current Status

## Version 3.0

Completed:

* Data integration pipeline
* Demographic integration
* Long-format dataset generation
* Wide-format dataset generation
* Inspiration4 quality-control framework
* Subject-level quality-control reporting
* Inter-subject variability analysis
* Baseline variability assessment
* Bed Rest overlap harmonization framework
* Locked overlap variable crosswalk
* LUNAR-compatible summary workbook generation

Current outputs:

* Inspiration4_Master_Long.csv
* Inspiration4_Master_Wide.csv
* Inspiration4_Data_Quality_Summary_V2.xlsx
* Inspiration4_BedRest_Overlap_Summary_v3_with_BUN.xlsx

Status:

* Analysis-ready
* Harmonized for comparison with Bed Rest Campaign 1
* Overlap biomarker framework established
* Prepared for future NHANES harmonization within the LUNAR framework

---

# Planned Analyses

Planned analyses include:

* Principal Component Analysis (PCA)
* Longitudinal trajectory modeling
* Biomarker correlation networks
* Immune profiling
* Clinical chemistry trend analysis
* Comparison with Bed Rest Campaign 1
* Comparison with NHANES terrestrial reference populations
* Cross-cohort harmonization within the LUNAR framework
* Development of common biomarker panels across astronaut, analog, and terrestrial populations

---

# Relationship to LUNAR

This dataset represents the first integrated astronaut cohort within the LUNAR project.

Future LUNAR analyses will compare Inspiration4 biomarker profiles with:

* Bed Rest Campaign 1
* Additional bed rest campaigns
* NHANES terrestrial reference populations
* Additional astronaut cohorts
* Future commercial spaceflight datasets

The long-term objective is to identify common and cohort-specific physiological responses associated with spaceflight, analog environments, and operationally relevant human performance stressors.

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
* Confirming variable harmonization
* Maintaining reproducible workflows
* Complying with all applicable data-use agreements and citation requirements

Derived datasets and summary products are intended to facilitate reproducible analysis within the LUNAR framework and do not replace the original source datasets.

