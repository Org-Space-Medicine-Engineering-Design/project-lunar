# Changelog

All notable changes to the active LUNAR workflow are documented here. The Data Challenge submission baseline is preserved separately by its release tag; later changes must not alter or redefine that record.

## Unreleased

Changes after the frozen baseline will be added here under an appropriate heading.

## hrp-data-challenge-v1.0.0 — Data Challenge submission baseline

### Fixed scientific scope

- Public-proxy demonstration using NHANES 1999–2018 as the terrestrial reference, UTMB Bed Rest Campaign 1 as the ground analog, and Inspiration4 as the operational spaceflight example.
- Seventeen harmonized biochemical variables evaluated at the participant-by-phase level.
- NHANES-referenced z-scores, Mahalanobis distance using the NHANES reference covariance matrix, and 1,000 reference-bootstrap resamples.
- No imputation of unavailable measurements; outputs are descriptive context, not causal or clinical conclusions.

### Frozen materials

- Repository code, configuration, documentation, data organization, and generated outputs at the release commit.
- Submission record described in `archive/hrp-data-challenge-v1.0/SUBMISSION_MANIFEST.md`.

### Post-submission policy

- Improvements must be made through a reviewed pull request to `main`.
- Method, input-data, output, or interpretation changes must be described in this file.
- The protected submission tag must never be moved, deleted, or used to represent later results.
