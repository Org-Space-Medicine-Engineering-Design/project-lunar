# LUNAR: Longitudinal Unification of Small-N Astronaut Responses

## NASA Human Research Program Data Challenge

> **Repository status**  
> `main` is the current development line. The submitted Data Challenge demonstration will be preserved as the protected release tag `hrp-data-challenge-v1.0.0` after the submission-baseline pull request is merged. Subsequent improvements belong in reviewed pull requests and must not be described as results of the original submission.

LUNAR is a reference-based framework for interpreting small, longitudinal astronaut biomedical datasets against a documented terrestrial reference population. It retains each participant-by-phase profile, provides marker-level context, and supplements it with a covariance-adjusted whole-profile distance.

## Data Challenge submission baseline

The submitted demonstration used publicly available proxy data:

| Role | Dataset | Submitted analytic cohort |
| --- | --- | --- |
| Terrestrial reference | NHANES 1999–2018 clinical chemistry | 59,882 complete biochemical profiles |
| Ground analog | UTMB Bed Rest Campaign 1 | 3 participants with complete profiles across study phases |
| Operational spaceflight example | Inspiration4 | 4 crewmembers with comparable pre- and post-flight profiles |

The locked shared panel contains 17 biochemical variables: albumin, globulin, albumin/globulin ratio, ALT, AST, BUN, creatinine, BUN/creatinine ratio, calcium, chloride, carbon dioxide, glucose, potassium, sodium, total protein, anion gap, and osmolality.

The baseline workflow:

1. Harmonizes compatible analytes, units, participant identifiers, and phases.
2. Calculates NHANES-referenced z-scores for marker-level interpretation.
3. Calculates Mahalanobis distance using the NHANES reference mean and covariance matrix for each complete participant-by-phase profile.
4. Uses 1,000 bootstrap resamples of the NHANES reference to assess stability of reference-derived outputs.

This proof of concept does not impute unavailable measurements, establish causal flight effects, diagnose clinical risk, or replace conventional statistics or clinical expertise.

The release manifest in [archive/hrp-data-challenge-v1.0/SUBMISSION_MANIFEST.md](archive/hrp-data-challenge-v1.0/SUBMISSION_MANIFEST.md) identifies what is fixed in the submission record and how later work should be documented.

## Repository structure

```text
project-lunar/
├── README.md                         # current project guide
├── CHANGELOG.md                      # baseline and post-submission changes
├── CONTRIBUTING.md                   # fork/branch/pull-request workflow
├── archive/
│   └── hrp-data-challenge-v1.0/      # submission manifest and supporting record
├── data/
│   ├── raw/                          # source-specific public proxy-data materials
│   └── processed/                    # analysis-ready derivatives
├── docs/                             # dataset and method documentation
├── notebooks/                        # exploratory/reproducible notebooks
├── output/                           # generated workbooks and figures
└── scripts/                          # preprocessing, harmonization, analysis, and figure code
```

## Reproducing the baseline

Create a Python environment, install the repository requirements, then run the documented source-specific preprocessing, cross-dataset analysis, and figure-generation scripts. The submission record is defined by the tagged commit and its files—not by later executions on changed data, code, or package versions.

```bash
python -m pip install -r requirements.txt
python scripts/cross_dataset/run_cross_dataset_analysis.py
python scripts/cross_dataset/run_figure_generation.py
```

Generated outputs are written under `output/`. The exact scripts and filenames may evolve after the baseline; post-submission changes must be recorded in [CHANGELOG.md](CHANGELOG.md).

## Collaboration

External contributors should work in a fork; maintainers may work in a feature branch in this repository. In either case:

1. Create one focused branch from current `main`.
2. Make a small, documented change.
3. Open a pull request to `main`.
4. Describe the scientific purpose, affected data or variables, validation performed, and documentation changes.
5. Wait for review before merging.

See [CONTRIBUTING.md](CONTRIBUTING.md) for the full workflow. A merge into `main` advances the active project; the protected Data Challenge tag remains the historical, reproducible baseline.

## AI usage statement

ChatGPT and Gemini within Google Colab were used as workflow, coding, troubleshooting, and documentation assistants during development of this demonstration. The LUNAR team directed and verified dataset selection, methodological decisions, code execution, quality control, data interpretation, and final submission materials.

## Team

Developed by the LUNAR team as a demonstration framework for the NASA Human Research Program Data Challenge.
