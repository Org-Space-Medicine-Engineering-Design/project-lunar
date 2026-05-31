# project-lunar
# Inspiration4 Integrated Biomedical Dataset

## Overview

This repository contains data integration scripts and derived datasets generated from publicly available Inspiration4 biomedical data. The goal of this project is to create analysis-ready datasets by combining clinical chemistry, multiplex biomarker, and demographic measurements into unified tables suitable for statistical analysis, machine learning, visualization, and longitudinal modeling.

The current release focuses on the Inspiration4 serum biomarker and clinical chemistry datasets.

---

## Repository Structure

```text
Inspiration4_Project/
│
├── data_raw/
│   └── Raw source CSV files (not included unless permitted)
│
├── outputs/
│   ├── Inspiration4_Master_Long.csv
│   └── Inspiration4_Master_Wide.csv
│
├── scripts/
│   └── combine_inspiration4_datasets.py
│
├── figures/
│
├── notebooks/
│
├── requirements.txt
│
└── README.md
```

---

## Source Data

The integrated dataset was generated from the following Inspiration4 data files:

* LSDS 8 Multiplex SerumSpaceX_serum_non_bridged
* LSDS 8 Multiplex Serum
* LSDS 8 Comprehensive Metabolic Panel (CMP)
* Demographics Inspiration4
* Additional serum biomarker datasets as available

These datasets contain:

* Clinical chemistry measurements
* Cytokines and inflammatory markers
* Cardiovascular biomarkers
* Immune biomarkers
* Demographic variables
* Longitudinal sampling information

Source data were obtained from publicly available Inspiration4 research datasets.

---

## Data Processing

The script:

```text
scripts/combine_inspiration4_datasets.py
```

performs the following operations:

1. Imports all source CSV files.
2. Standardizes column names.
3. Harmonizes participant identifiers.
4. Harmonizes collection timepoints.
5. Merges demographic information.
6. Combines biomarker panels into a unified structure.
7. Generates both long-format and wide-format analysis datasets.

---

## Outputs

### Inspiration4_Master_Long.csv

Long-format dataset suitable for:

* Longitudinal modeling
* Mixed-effects analyses
* Repeated measures statistics
* Data visualization

Dimensions:

```text
8,252 rows × 14 columns
```

Each row represents an individual measurement.

---

### Inspiration4_Master_Wide.csv

Wide-format dataset suitable for:

* Principal Component Analysis (PCA)
* Machine learning workflows
* Correlation analysis
* Clustering
* Multivariate statistics

Dimensions:

```text
28 rows × 304 columns
```

Each row represents a participant-timepoint observation.

---

## Software Requirements

Python version:

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
pip install -r requirements.txt
```

---

## Running the Pipeline

Place source files in:

```text
data_raw/
```

Run:

```bash
python scripts/combine_inspiration4_datasets.py
```

Generated files will be written to:

```text
outputs/
```

---

## Dataset Version History

### v1.0 (2026-05-31)

Initial integrated Inspiration4 biomedical dataset.

Included:

* Multiplex serum biomarker data
* Comprehensive Metabolic Panel (CMP) data
* Demographic data
* Long-format integrated dataset
* Wide-format integrated dataset
* Data integration script

Outputs:

* Inspiration4_Master_Long.csv
* Inspiration4_Master_Wide.csv

Dataset dimensions:

* Long: 8,252 rows × 14 columns
* Wide: 28 rows × 304 columns

---

## Planned Analyses

Future analyses may include:

* Principal Component Analysis (PCA)
* Longitudinal trajectory analysis
* Mixed-effects modeling
* Biomarker correlation networks
* Heatmaps and clustering
* Cytokine and immune profiling
* Clinical chemistry trend analysis
* Cross-dataset integration with additional Inspiration4 and LSDA datasets

---

## Citation

If using this repository or derived datasets, please cite the original Inspiration4 data source and associated publications where applicable.

---

## Disclaimer

This repository contains derived research datasets generated from publicly available source data. Users are responsible for verifying all analyses and ensuring compliance with applicable data-use agreements and citation requirements.
