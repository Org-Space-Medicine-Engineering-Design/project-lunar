Bed Rest Campaign 1 Biomedical Dataset
Overview
This folder contains the Bed Rest Campaign 1 datasets, processing scripts, derived datasets, harmonization products, and quality-control reports generated as part of the LUNAR (Longitudinal Unification of Small-N Astronaut Responses) project.
The purpose of this dataset is to create analysis-ready biomedical data products from UTMB Bed Rest Campaign 1 that can be directly compared with astronaut cohorts (e.g., Inspiration4) and terrestrial reference populations (e.g., NHANES).
The Bed Rest Campaign 1 dataset serves as the primary spaceflight analog cohort currently integrated into the LUNAR framework.
________________________________________
Source Data
The integrated datasets were generated from the raw UTMB Bed Rest Campaign 1 CSV files.
Input source:
•	Campaign 1 raw data archive
•	27 Campaign 1 CSV files
The workflow supports either:
•	A ZIP archive containing all Campaign 1 CSV files
•	An extracted directory containing all Campaign 1 CSV files
These datasets include:
•	Clinical chemistry measurements
•	Laboratory biomarkers
•	Participant identifiers
•	Test phase information
•	Multiple collection timepoints throughout the bed rest campaign
________________________________________
Cohort Description
The current overlap cohort contains three clinical chemistry participants:
•	C1G0001
•	C1G0002
•	C1G0003
Other identifiers may appear in the raw Campaign 1 files but represent:
•	Sample identifiers
•	Group identifiers
•	Non-overlap participants
•	Study-specific identifiers
Only the three overlap cohort participants are retained in the harmonized overlap datasets.
________________________________________
Processing Pipeline
build_bedrest_campaign1_overlap_summary.py
This script generates the harmonized overlap dataset and quality-control workbook from the raw Campaign 1 files.
Inputs:
•	Campaign 1 ZIP archive or extracted directory
The script:
1.	Loads all Campaign 1 source files.
2.	Harmonizes variable names.
3.	Identifies overlap variables shared with Inspiration4.
4.	Generates derived variables.
5.	Produces a long-format master dataset.
6.	Produces a harmonized overlap dataset.
7.	Generates a comprehensive quality-control workbook.
Run:
python scripts/build_bedrest_campaign1_overlap_summary.py \
    --input "data/raw/bed_rest_campaign1/Campaign 1-20260603T141236Z-3-001.zip" \
    --output-dir "outputs/bed_rest_campaign1" \
    --prefix "LUNAR_BedRest_Campaign1_OVERLAP_v3"
Outputs:
•	LUNAR_BedRest_Campaign1_OVERLAP_v3_Master_Long.csv
•	LUNAR_BedRest_Campaign1_OVERLAP_v3_Overlap_Data.csv
•	LUNAR_BedRest_Campaign1_OVERLAP_Summary_v3.xlsx
________________________________________
generate_bedrest_timepoint_binning.py
This script generates a harmonized phase-binned workbook from the Bed Rest overlap dataset.
Input:
•	LUNAR_BedRest_Campaign1_OVERLAP_Summary_v3.xlsx
Required sheet:
•	Overlap_Data
Required columns:
•	Subject_ID
•	Test_Phase
•	Value_Numeric
•	Inspiration4_Variable
Run:
python scripts/generate_bedrest_timepoint_binning.py \
    --input outputs/bed_rest_campaign1/LUNAR_BedRest_Campaign1_OVERLAP_Summary_v3.xlsx \
    --output outputs/bed_rest_campaign1/BedRest_Timepoint_Binning_Workbook.xlsx
Purpose
The script creates a workbook structure aligned with the Inspiration4 harmonization workbook.
Repeated measurements within each phase are averaged:
•	PRE_TEST → Pre_BedRest
•	IN_TEST → In_BedRest
•	POST_TEST → Post_BedRest
This provides a harmonized framework for comparison between:
•	Bed Rest Campaign 1
•	Inspiration4
•	NHANES
Generated Workbook
Output:
•	BedRest_Timepoint_Binning_Workbook.xlsx
The workbook contains one worksheet per overlap biomarker.
Each worksheet includes:
Raw Phase Means
Participant-level averages for:
•	Pre_BedRest
•	In_BedRest
•	Post_BedRest
________________________________________
Subject-Level Summary
For each participant:
•	Pre_BedRest value
•	In_BedRest value
•	Post_BedRest value
•	Post–Pre Delta
•	Percent Delta
________________________________________
Cohort Summary Worksheet
The workbook contains a Cohort_Summary worksheet reporting:
•	Pre_BedRest Mean
•	Pre_BedRest SD
•	In_BedRest Mean
•	In_BedRest SD
•	Post_BedRest Mean
•	Post_BedRest SD
•	Delta Mean
•	Delta SD
•	Percent Delta Mean
•	Percent Delta SD
•	Subject counts
________________________________________
Overlap Variables
The final overlap set contains 18 variables.
Measured Variables
•	ALBUMIN
•	ALKALINE PHOSPHATASE
•	ALT
•	AST
•	BILIRUBIN; TOTAL
•	CALCIUM
•	CARBON DIOXIDE
•	CHLORIDE
•	CREATININE
•	CRP
•	GLUCOSE
•	POTASSIUM
•	PROTEIN; TOTAL
•	SODIUM
•	UREA NITROGEN (BUN)
Derived Variables
•	GLOBULIN
•	ALBUMIN/GLOBULIN RATIO
•	BUN/CREATININE RATIO
________________________________________
Derived Variable Rules
Three variables are calculated because they are present in the Inspiration4 overlap dataset and can be derived from measured Bed Rest values.
Globulin
GLOBULIN = PROTEIN; TOTAL − ALBUMIN
Unit:
g/dL
________________________________________
Albumin/Globulin Ratio
ALBUMIN/GLOBULIN RATIO = ALBUMIN / GLOBULIN
Unit:
ratio
________________________________________
BUN/Creatinine Ratio
BUN/CREATININE RATIO = UREA NITROGEN (BUN) / CREATININE
Unit:
ratio
Quality-control rule:
Only blood/serum creatinine values from the Flight Chemistry dataset are used when calculating BUN/CREATININE RATIO.
Urine creatinine and creatinine clearance measurements are excluded.
________________________________________
Available Outputs
LUNAR_BedRest_Campaign1_OVERLAP_v3_Master_Long.csv
Full Campaign 1 long-format dataset generated from all source files.
Characteristics:
•	One row per observation
•	Includes all source-file variables
•	Useful for auditing
•	Useful for troubleshooting
•	Not limited to overlap variables
________________________________________
LUNAR_BedRest_Campaign1_OVERLAP_v3_Overlap_Data.csv
Analysis-ready overlap dataset.
Characteristics:
•	One row per observation
•	Contains only overlap variables
•	Includes derived variables
•	Supports harmonization workflows
________________________________________
LUNAR_BedRest_Campaign1_OVERLAP_Summary_v3.xlsx
Comprehensive overlap summary workbook.
Workbook tabs include:
•	Dataset_Inventory
•	Variable_Stats
•	Variable_Stats_By_Timepoint
•	Subject_Stats
•	Subject_Timepoint_Variable_Stat
•	Subject_Missingness
•	Subject_Timepoint_Stats
•	Missing_By_Variable
•	Missing_By_Timepoint
•	Overlap_Crosswalk
•	Units_Audit
•	Derived_Variables_Audit
•	Participant_Audit
•	Overlap_Data
Characteristics:
•	Generated from harmonized overlap data
•	Includes overlap crosswalk documentation
•	Includes quality-control reporting
•	Includes coverage assessment
•	Includes participant auditing
________________________________________
BedRest_Timepoint_Binning_Workbook.xlsx
Phase-binned harmonization workbook.
Contains:
•	One worksheet per overlap biomarker
•	Participant-level phase averages
•	Participant-level delta calculations
•	Cohort-level summary worksheet
•	Percent-change calculations
Primary use:
•	Cross-cohort harmonization
________________________________________
Missingness Method
Missingness is calculated using expected coverage across:
Subject × Test_Phase × Overlap Variable
Expected phases:
•	PRE_TEST
•	IN_TEST
•	POST_TEST
A variable is considered present when at least one numeric value exists for a given:
•	Subject
•	Test phase
•	Variable
combination.
________________________________________
Summary Statistics Method
Summary statistics are calculated using numeric values only.
Reported statistics include:
•	N
•	Mean
•	SD
•	Median
•	Min
•	Q1
•	Q3
•	IQR
•	Max
Non-numeric observations are retained where appropriate for audit purposes but do not contribute to numerical summaries.
________________________________________
Cohort Summary
Study:
•	UTMB Bed Rest Campaign 1
Overlap Cohort Size:
•	3 participants
Primary Phases:
•	PRE_TEST
•	IN_TEST
•	POST_TEST
Data Domains:
•	Clinical chemistry
•	Inflammatory biomarkers
•	Laboratory biomarkers
•	Derived chemistry variables
________________________________________
Recommended Files
Data Exploration
Use:
•	LUNAR_BedRest_Campaign1_OVERLAP_v3_Overlap_Data.csv
Recommended uses:
•	Review participant-level observations
•	Verify variable coverage
•	Explore phase distributions
•	Assess overlap variables
________________________________________
Data Quality Assessment
Use:
•	LUNAR_BedRest_Campaign1_OVERLAP_Summary_v3.xlsx
Recommended uses:
•	Missingness assessment
•	Participant-level quality control
•	Variable-level quality control
•	Unit verification
•	Cohort characterization
________________________________________
Longitudinal Harmonization
Use:
•	BedRest_Timepoint_Binning_Workbook.xlsx
Recommended uses:
•	Pre-versus-post bed rest comparisons
•	Cohort summary generation
•	Cross-cohort harmonization
•	Inspiration4 comparison
•	NHANES comparison
________________________________________
Relationship to LUNAR
This dataset represents the first spaceflight analog cohort integrated into the LUNAR project.
The overlap variables were intentionally harmonized to match the Inspiration4 overlap framework.
Shared reporting elements include:
•	Dataset inventory
•	Variable summary statistics
•	Missingness assessment
•	Participant audits
•	Units audits
•	Derived variable audits
•	Cohort summary statistics
•	Harmonized overlap variable definitions
The phase-binned workbook was designed to align structurally with the Inspiration4 timepoint-binning workbook to facilitate direct comparison across astronaut, analog, and terrestrial datasets.
________________________________________
Current Status
Version 4.0
Completed:
•	Campaign 1 raw data ingestion
•	Long-format master dataset generation
•	Inspiration4 overlap variable harmonization
•	Derived variable generation
•	Quality-control reporting framework
•	Participant audit framework
•	Missingness reporting framework
•	Overlap summary workbook generation
•	Bed Rest phase binning framework
•	Cohort-level summary statistic generation
•	Harmonization with Inspiration4 overlap variables
•	Harmonization with NHANES overlap variables
•	LUNAR-compatible reporting framework
Current outputs:
•	LUNAR_BedRest_Campaign1_OVERLAP_v3_Master_Long.csv
•	LUNAR_BedRest_Campaign1_OVERLAP_v3_Overlap_Data.csv
•	LUNAR_BedRest_Campaign1_OVERLAP_Summary_v3.xlsx
•	BedRest_Timepoint_Binning_Workbook.xlsx
Status:
•	Data integration complete
•	Overlap harmonization complete
•	Derived variable generation complete
•	Quality-control reporting complete
•	Phase binning complete
•	Cohort summary generation complete
•	Harmonized for comparison with Inspiration4
•	Harmonized for comparison with NHANES
•	Integrated into the LUNAR framework
________________________________________
Citation
If using this dataset or derived products, please cite:
•	Original UTMB Bed Rest Campaign 1 data sources
•	Associated Bed Rest Campaign publications
•	Any downstream analyses generated from these harmonized datasets
________________________________________
Disclaimer
This folder contains derived datasets generated from Bed Rest Campaign 1 source data.
Users are responsible for:
•	Verifying analyses
•	Validating results
•	Confirming interpretation of derived variables
•	Ensuring compliance with original data-use requirements

