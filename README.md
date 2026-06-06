# LUNAR: Longitudinal Unification of Small-N Astronaut Responses

## NASA Human Research Program Data Challenge – Component 2 Demonstration Using Proxy Data

### Overview

LUNAR (Longitudinal Unification of Small-N Astronaut Responses) is a data integration and analysis framework designed to compare small, longitudinal astronaut biomedical datasets against larger terrestrial reference populations. The framework addresses a common challenge in spaceflight human research: deriving meaningful biological context from limited astronaut sample sizes by leveraging harmonized comparison cohorts and multivariate analytical methods.

This demonstration applies the LUNAR methodology to publicly available proxy datasets representing:

* A terrestrial reference population derived from the National Health and Nutrition Examination Survey (NHANES)
* A commercial astronaut cohort from Inspiration4
* A ground-based spaceflight analog cohort from a long-duration bed rest campaign

The objective of this demonstration is to show how longitudinal astronaut and analog biomedical data can be standardized, harmonized, and compared within a unified analytical framework capable of supporting future deep-space human health monitoring applications.

---

## Repository Structure

```text
project-lunar-main/
│
├── README.md
├── requirements.txt
│
├── data/
│   ├── raw/
│   │   ├── NHANES/
│   │   ├── Inspiration4/
│   │   └── BedRest/
│   │
│   └── processed/
│
├── scripts/
│   └── cross_dataset/
│
├── notebooks/
│
├── docs/
│
└── output/
```

---

## Included Proxy Datasets

### NHANES Reference Cohort

The NHANES dataset serves as the terrestrial reference population and contains clinical laboratory measurements collected from a large, representative sample of U.S. adults.

Purpose within LUNAR:

* Establish population-level biomarker distributions
* Define reference means and standard deviations
* Support standardized deviation calculations
* Provide a baseline for comparison against astronaut and analog cohorts

Additional dataset documentation is available in:

```text
data/raw/NHANES/README.md
```

---

### Inspiration4 Cohort

The Inspiration4 dataset contains longitudinal biomedical measurements collected from commercial astronauts before and after orbital spaceflight.

Purpose within LUNAR:

* Demonstrate astronaut-specific application of the framework
* Evaluate biomarker deviations relative to terrestrial norms
* Assess whole-profile physiological changes across mission phases

Additional dataset documentation is available in:

```text
data/raw/Inspiration4/README.md
```

---

### Bed Rest Analog Cohort

The bed rest dataset contains longitudinal biomedical measurements collected during a controlled ground-based spaceflight analog campaign.

Purpose within LUNAR:

* Demonstrate applicability to analog environments
* Compare physiological adaptations with those observed in astronaut cohorts
* Evaluate framework performance across independent longitudinal datasets

Additional dataset documentation is available in:

```text
data/raw/BedRest/README.md
```

---

## Methodological Overview

### 1. Variable Harmonization

Clinical laboratory variables common to the included datasets were identified through a structured overlap assessment.

Variables were standardized to:

* Common naming conventions
* Consistent measurement units
* Harmonized biomarker definitions

Only biomarkers available across comparison cohorts were retained for downstream analyses.

---

### 2. Cohort Summary Generation

For each harmonized biomarker, descriptive statistics were generated including:

* Sample size (N)
* Mean
* Median
* Standard deviation
* Minimum
* Maximum

These summaries support data quality evaluation and provide an overview of each cohort.

---

### 3. Standardized Deviation Scoring

Individual biomarker values were compared against NHANES-derived reference distributions.

Standardized deviation scores were calculated to quantify departures from terrestrial reference values while enabling comparison across biomarkers measured on different scales and units.

---

### 4. Multivariate Distance Integration

Individual biomarker deviations were integrated into a global physiological profile score.

The LUNAR framework utilizes Mahalanobis distance as the primary multivariate distance metric because it:

* Accounts for differences in biomarker scales and units
* Incorporates covariance among biomarkers
* Prevents over-weighting of correlated variables
* Produces a whole-profile measure of physiological deviation

Distances are calculated relative to the NHANES reference distribution.

---

### 5. Bootstrap Pseudo-Crew Sensitivity Analysis

Given the small sample sizes typically available in astronaut research, a bootstrap pseudo-crew approach was implemented to evaluate methodological sensitivity and robustness.

Random subsets of NHANES participants are repeatedly sampled to generate simulated crews of varying sizes. This process demonstrates how multivariate distance metrics behave under astronaut-relevant sample sizes and provides insight into expected variability associated with small-N cohorts.

---

## Software Requirements and Installation

Analyses were developed and tested using Python 3.11 or later.

### Required Packages

The demonstration requires the following Python packages:

* pandas
* numpy
* scipy
* scikit-learn
* openpyxl
* matplotlib
* jupyter

Install all dependencies using:

```bash
python -m pip install -r requirements.txt
```

Alternatively, packages may be installed individually:

```bash
python -m pip install pandas numpy scipy scikit-learn openpyxl matplotlib jupyter
```

---

## Reproducing the Demonstration

The following workflow reproduces the primary analyses and outputs included in this submission.

### Step 1: Extract the Repository

Download or extract the repository contents to a local directory.

### Step 2: Navigate to the Repository Root

```bash
cd project-lunar-main
```

### Step 3: Install Dependencies

Install all required packages using:

```bash
python -m pip install -r requirements.txt
```

This step ensures that all required libraries are available, including NumPy, SciPy, scikit-learn, pandas, matplotlib, and openpyxl.

### Step 4: Run the Cross-Dataset Analysis

```bash
python scripts/cross_dataset/run_cross_dataset_analysis.py
```

This script generates:

* Cohort summary workbooks
* Dataset overlap assessments
* Harmonized comparison datasets

### Step 5: Generate Figures and Visualizations

```bash
python scripts/cross_dataset/run_figure_generation.py
```

This script generates:

* Heatmaps
* Cohort comparison figures
* Additional demonstration visualizations

### Step 6: Review Outputs

Generated files will be written to:

```text
output/
```

including summary workbooks, comparison tables, figures, and supporting analytical outputs.

---

## Verification and Reproducibility

Successful execution should complete without errors and generate output files within the `output/` directory.

Representative outputs include:

```text
output/

├── LUNAR_NHANES_Data_Quality_Summary.xlsx
├── LUNAR_NHANES_OVERLAP_Summary.xlsx
├── LUNAR_Inspiration4_OVERLAP_Summary.xlsx
├── LUNAR_BedRest_OVERLAP_Summary.xlsx
├── Mahalanobis_Distance_Results.xlsx
├── Bootstrap_Sensitivity_Results.xlsx
└── Figures/
```

Specific filenames may vary depending on the workflow executed.

All analyses were developed using relative file paths and should execute without modification when the repository structure is preserved. Running the scripts described above will reproduce the demonstration results included in this submission.

No proprietary software is required.

---

## AI Usage Statement

ChatGPT (OpenAI GPT-5.5 Thinking) and Gemini within Google Colab were used as workflow, coding, troubleshooting, and documentation assistants during development of this demonstration. These tools were used to support code organization, debugging, README preparation, workflow planning, documentation formatting, and discussion of analytical approaches. All dataset selection, methodological decisions, code execution, quality control, data interpretation, and final submission materials were reviewed, validated, and directed by the LUNAR team. AI-generated content served only as draft support and was verified against source data, project requirements, and team guidance prior to inclusion.

---

## Team

**LUNAR – Longitudinal Unification of Small-N Astronaut Responses**

Developed as a demonstration framework for the NASA Human Research Program Data Challenge to explore scalable approaches for integrating astronaut, analog, and terrestrial biomedical datasets within a unified analytical environment.
