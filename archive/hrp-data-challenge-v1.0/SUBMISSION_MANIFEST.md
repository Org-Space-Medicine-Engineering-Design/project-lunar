# LUNAR Data Challenge submission manifest

## Purpose

This directory documents the exact scientific scope that will be frozen by GitHub release tag `hrp-data-challenge-v1.0.0`. The tag must point to the `main` merge commit that introduces this manifest, README status statement, CHANGELOG, and contribution workflow.

A future branch or pull request may improve LUNAR, but it must not modify this tag or characterize changed methods or results as part of the Data Challenge submission.

## Submitted demonstration

| Element | Fixed baseline |
| --- | --- |
| Reference population | NHANES 1999–2018, 59,882 complete biochemical profiles |
| Ground analog | UTMB Bed Rest Campaign 1, 3 complete-profile participants |
| Operational spaceflight example | Inspiration4, 4 crewmembers with comparable pre- and post-flight profiles |
| Shared panel | 17 harmonized biochemical variables |
| Marker-level output | NHANES-referenced z-scores |
| Profile-level output | Mahalanobis distance calculated from the NHANES reference mean and covariance matrix |
| Sensitivity analysis | 1,000 bootstrap resamples of the NHANES reference |

## Fixed interpretation boundary

- Each observation remains a participant-by-phase profile; the framework does not reduce the demonstration to cohort averages alone.
- Only measurements that can be validly harmonized by analyte definition and unit are included.
- Missing measurements are not imputed.
- Observed deviations are descriptive reference-based context. They do not establish causality, clinical abnormality, operational readiness, or clinical risk.

## Repository materials captured by the release

- Source-specific data organization and documentation under `data/` and `docs/`.
- Preprocessing, harmonization, analysis, bootstrap, and figure-generation code under `scripts/` and `notebooks/`.
- Repository requirements, outputs, figures, and workbooks present at the release commit.
- This manifest, the root README, and `CHANGELOG.md`.

## Release procedure

1. Merge the reviewed submission-baseline pull request to `main`.
2. Draft a GitHub release with new tag `hrp-data-challenge-v1.0.0` targeted to that merge commit.
3. Title the release **LUNAR — NASA HRP Data Challenge submission baseline** and state that it is immutable.
4. Add a tag ruleset for `hrp-data-challenge-*` that blocks tag updates and deletion.
5. Protect `main` so subsequent work enters by pull request and approval.

## After the release

New work belongs on a feature branch or a fork and should target `main` through a pull request. Record material changes in `CHANGELOG.md`; cite the release tag whenever distinguishing the original submission from later analyses.
