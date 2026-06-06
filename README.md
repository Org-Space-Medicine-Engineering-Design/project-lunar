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
LUNAR/
│
├── README.md
│
├── code/
│   ├── *.py
│   └── *.ipynb
│
├── data/
│   ├── raw/
│   │   ├── NHANES/
│   │   │   ├── README.md
│   │   │   └── ...
│   │   │
│   │   ├── Inspiration4/
│   │   │   ├── README.md
│   │   │   └── ...
│   │   │
│   │   └── BedRest/
│   │       ├── README.md
│   │       └── ...
│   │
│   └── processed/
│
└── outputs/
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

## Software Requirements

Analyses were developed and tested using:

```text
Python 3.11+
```

Primary packages include:

```text
pandas
numpy
scipy
scikit-learn
openpyxl
matplotlib
jupyter
```

Required packages can be installed using:

```bash
pip install -r requirements.txt
```

---

## Running the Demonstration

### Step 1

Clone or extract the repository.

### Step 2

Open a terminal and navigate to the repository root directory.

### Step 3

Install required packages.

```bash
pip install -r requirements.txt
```

### Step 4

Execute the analysis workflow.

Example:

```bash
python lunar_pipeline.py
```

Alternatively, open the provided Jupyter notebook and execute all cells from top to bottom.

```bash
jupyter notebook
```

---

## Expected Outputs

Successful execution will generate summary tables, figures, and Excel workbooks in the `outputs/` directory.

Representative outputs include:

```text
outputs/

├── Cohort_Summary.xlsx
├── NHANES_Overlap_Summary.xlsx
├── Inspiration4_Overlap_Summary.xlsx
├── BedRest_Overlap_Summary.xlsx
├── Mahalanobis_Distance_Results.xlsx
├── Bootstrap_Sensitivity_Results.xlsx
└── Figures/
```

Specific filenames may vary depending on the workflow executed.

---

## Reproducibility Statement

All analyses included in this submission are fully reproducible using the provided proxy datasets and code.

Running the analysis workflows from start to finish using the instructions above will regenerate all reported summary tables, Excel workbooks, and figures without requiring modification of the source code.

No proprietary software is required.

---

## AI Usage Statement

ChatGPT (OpenAI GPT-5.5 Thinking) and Gemini within Google Colab were used as workflow, coding, troubleshooting, and documentation assistants during development of this demonstration. These tools were used to support code organization, debugging, README preparation, workflow planning, documentation formatting, and discussion of analytical approaches. All dataset selection, methodological decisions, code execution, quality control, data interpretation, and final submission materials were reviewed, validated, and directed by the LUNAR team. AI-generated content served only as draft support and was verified against source data, project requirements, and team guidance prior to inclusion.

---

## Team

**LUNAR – Longitudinal Unification of Small-N Astronaut Responses**

Developed as a demonstration framework for the NASA Human Research Program Data Challenge to explore scalable approaches for integrating astronaut, analog, and terrestrial biomedical datasets within a unified analytical environment.
