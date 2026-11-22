# Contributing to LUNAR

## Protect the submission record

The release tag `hrp-data-challenge-v1.0.0` represents the submitted NASA Human Research Program Data Challenge demonstration. Do not rewrite history, move that tag, or present later results as submission results. Develop new work from current `main` and document meaningful changes in `CHANGELOG.md`.

## Fork-and-pull-request workflow

1. Click **Fork** to create a personal copy of `Org-Space-Medicine-Engineering-Design/project-lunar`.
2. In the fork, create one focused branch from current `main`, such as `feature/missingness-simulation` or `docs/data-source-map`.
3. Make and commit your changes on that branch. Keep unrelated changes out of the same pull request.
4. Sync the fork with upstream `main` before opening a pull request when practical.
5. Open a pull request with base repository `Org-Space-Medicine-Engineering-Design/project-lunar` and base branch `main`.
6. Respond to review comments; only an approved pull request may be merged.

Maintainers with write access may create a feature branch in this repository instead of a fork, but the pull-request and review requirements still apply.

## Pull-request expectations

Every pull request should state:

- The scientific or technical purpose and the subgroup/workstream it supports.
- Files, data sources, variables, or assumptions affected.
- Validation performed: reproduction command, notebook, output comparison, or reason validation is not applicable.
- Whether results, figures, documentation, dependencies, or the interpretation boundary changed.
- A `CHANGELOG.md` update for any change that affects method, inputs, outputs, or interpretation.

## Data and scientific safeguards

- Use only data that may be shared in this public repository; preserve source provenance and access restrictions.
- Do not overwrite raw inputs or generated baseline outputs without documenting why and how the change was validated.
- Preserve the participant-by-phase structure and report missingness rather than silently imputing unavailable measurements.
- Treat z-scores and Mahalanobis distance as descriptive reference-based outputs, not diagnoses, causal estimates, or operational risk scores.

## Review and merge

Maintainers review the diff, validation evidence, documentation, and changelog. A merge advances the active `main` branch only; the protected Data Challenge tag remains the historical baseline.
