# LUNAR: Longitudinal Unification of Small-N Astronaut Responses

## Overview

LUNAR (Longitudinal Unification of Small-N Astronaut Responses) is a biomedical data harmonization and analytical framework designed to compare astronaut, spaceflight analog, and terrestrial reference populations using standardized clinical chemistry biomarkers.

The current implementation integrates:

1. NHANES terrestrial reference population
2. Inspiration4 commercial astronaut cohort
3. UTMB Bed Rest Campaign 1 analog cohort

The objective is to identify common physiological patterns across spaceflight and spaceflight analog environments while providing a statistically robust terrestrial reference population for comparison.

---

# Project Structure

```text
data/
├── nhanes/
├── inspiration4/
└── bedrest_campaign1/

scripts/
├── nhanes/
├── inspiration4/
├── bedrest/
└── cross_dataset/

outputs/
├── workbooks/
├── figures/
└── datasets/

notebooks/
```

---

# Datasets

## NHANES

NHANES serves as the terrestrial reference population.

Characteristics:

* 73,170 observations
* 72,624 unique participants
* Multiple survey cycles
* Cross-sectional design

Primary output:

```text
nhanes_biopro_all_cycles_combined.csv
```

---

## Inspiration4

Inspiration4 represents the first astronaut cohort integrated into LUNAR.

Participants:

* C001
* C002
* C003
* C004

Sampling schedule:

* L-92
* L-44
* L-3
* R+1
* R+45
* R+82
* R+194

Primary outputs:

```text
Inspiration4_Master_Long.csv
Inspiration4_Master_Wide.csv
```

---

## UTMB Bed Rest Campaign 1

Bed Rest Campaign 1 serves as the primary spaceflight analog cohort.

Participants:

* C1G0001
* C1G0002
* C1G0003

Primary phases:

* PRE_TEST
* IN_TEST
* POST_TEST

Primary output:

```text
Campaign1_Master_Long_REAL.xlsx
```

---

# Harmonization Framework

## Overlap Variable Set

The harmonization framework identified 18 overlapping clinical chemistry biomarkers.

Measured variables:

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

Derived variables:

* Globulin
* Albumin/Globulin Ratio
* BUN/Creatinine Ratio

Total overlap variables:

18

---

# Final Statistical Panel

The overlap framework contains 18 biomarkers.

However, the final statistical and multivariate analyses use a locked 17-variable panel.

CRP was excluded from:

* Z-score analyses
* Repeated-measures analyses
* Mahalanobis distance analyses
* Bootstrap sensitivity analyses

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

# Statistical Workflow

## NHANES Normalization

All astronaut and bed-rest observations are transformed into NHANES-referenced z-scores:

z = (x − μNHANES) / σNHANES

where:

* x = observed value
* μNHANES = NHANES mean
* σNHANES = NHANES standard deviation

---

## Cross-Dataset Statistics

Analyses include:

* One-sample tests against NHANES reference
* Welch comparisons between cohorts
* Paired longitudinal tests
* Repeated-measures ANOVA
* Benjamini-Hochberg FDR correction

Primary output:

```text
LUNAR_Final18_Statistical_Comparison_Workbook.xlsx
```

---

# Multivariate Analysis

## Primary Analysis

Whole-reference Mahalanobis distance.

Output:

```text
LUNAR_Mahalanobis_Full_NHANES_Reference.xlsx
```

This implementation uses the entire NHANES reference population to estimate the covariance structure and centroid.

---

## Sensitivity Analysis

Bootstrap pseudo-reference cohorts.

Output:

```text
mahalanobis_distance_summary.xlsx
```

The bootstrap framework evaluates the sensitivity of Mahalanobis distance estimates to sampling variation within the NHANES reference population.

---

# Final Outputs

## Workbooks

* LUNAR_NHANES_Data_Quality_Summary_v4.xlsx
* LUNAR_NHANES_OVERLAP_Summary_v2.xlsx
* Inspiration4_Data_Quality_Summary_v2_SubjectStats.xlsx
* LUNAR_Inspiration4_OVERLAP_Summary_v1.xlsx
* Inspiration4_Timepoint_Binning_Workbook_All3_Summaries.xlsx
* Campaign1_Data_Quality_Summary_REAL.xlsx
* LUNAR_BedRest_Campaign1_OVERLAP_Summary_v3.xlsx
* BedRest_Timepoint_Binning_Workbook.xlsx
* LUNAR_Final18_Statistical_Comparison_Workbook.xlsx
* LUNAR_Mahalanobis_Full_NHANES_Reference.xlsx
* mahalanobis_distance_summary.xlsx

## Figures

* Figure_01_Zscore_Heatmaps.png
* Figure_02_FullReference_Mahalanobis_Trajectories.png
* Figure_03_Bootstrap_Mahalanobis_KDE.png
* Figure_04_Bootstrap_Mahalanobis_Violin.png

---

# Current Status

Completed:

* NHANES harmonization
* Inspiration4 harmonization
* Bed Rest harmonization
* Overlap variable framework
* Derived variable generation
* Data-quality reporting
* Cross-dataset statistical analyses
* NHANES-referenced z-score analyses
* Whole-reference Mahalanobis analyses
* Bootstrap sensitivity analyses
* Publication-ready figures

Status:

Analytical framework complete.
