---
name: stata-experiment-hardening
description: Run and debug Stata empirical workflows on Windows with reproducible FE/DID outputs. Use when Codex needs to execute or fix .do pipelines, verify treatment coding, enforce firm+year FE specifications, resolve path or encoding issues (especially Chinese paths), stabilize postfile or permute extraction, and sync tables/docs deliverables.
---

# Stata Experiment Hardening

## Quick Start
1. Confirm the research contract before coding: unit of analysis, FE pair, clustering level, and core treatment variable.
2. Harden Windows paths and encoding first; do not start regression before this passes.
3. Run baseline and robustness blocks separately; persist every output table immediately.
4. Validate coding, estimation, and exported artifacts with the QA gate before writing conclusions.
5. Load [references/stata-twfe-checklist.md](references/stata-twfe-checklist.md) for command templates.

## Workflow

### 1) Lock model contract
- Record target specification in one line: `Y_it = beta*DID_ct + controls + firm FE + year FE`.
- Reject ambiguous statements like "city and year FE" when the thesis target is firm-level FE.
- Define primary table columns before running (baseline, controls, clustering change, sensitivity only).

### 2) Harden execution environment
- Map a temporary ASCII drive letter to avoid Chinese-path breakage in Stata/Python.
- Route logs/tables/figures through that mapped path.
- Prefer Stata auto-detected encoding when `encoding("utf8")` causes unexpected import failures.

### 3) Validate data and treatment coding
- Check policy assignment at the intended geography-year level before any regression.
- Verify treatment timing transitions explicitly (e.g., 2020 pilot provinces, 2021 national rollout).
- Fail fast if mixed coding exists within a geography-year cell.

### 4) Run FE regressions with extraction safety
- Run TWFE baseline first (`firm FE + year FE`), then add controls and robustness changes.
- Capture `r(b) r(t) r(p)` into locals immediately after extraction; do not let later commands overwrite `r()`.
- Treat absorbed variables as valid outcomes and report as collinearity/absorption, not as missing work.

### 5) Stabilize placebo and post-processing
- In `permute` output, detect generated variables by pattern (`_pm*`) instead of hard-coded names.
- Compute empirical placebo p-value from detected permutation variable, not guessed column names.
- Keep each table writer independent (`postfile/postclose` blocks must not share mutable state).

### 6) Sync deliverables
- Export tables to canonical output directory first.
- Mirror outputs to every delivery copy that the project keeps (analysis, docx_work, final delivery tree).
- Update narrative documents only after table regeneration completes.

### 7) QA gate (must pass before conclusion)
- Confirm FE pair and clustering match the thesis requirement.
- Confirm baseline coefficients and signs are consistent across reruns.
- Confirm significance claims are based on main specification, not sensitivity-only columns.
- Confirm links/paths in docs are valid and clickable when requested.

## Failure Patterns and Fixes From This Project
- Symptom: path or file-not-found with Chinese directories. Fix: map `X:` to project root and run all Stata I/O via `X:/...`.
- Symptom: CSV import fails with forced UTF-8 argument. Fix: remove explicit `encoding()` and let Stata auto-detect.
- Symptom: all t-stats in a table become identical or zero. Fix: store returned scalars into locals before `post`.
- Symptom: placebo p-value missing after `permute`. Fix: use `ds _pm*` to discover actual permutation variable.
- Symptom: conclusion depends only on linear trend column. Fix: treat as sensitivity result; keep TWFE baseline as main inference.
- Symptom: document Chinese text turns into `?`. Fix: edit through UTF-8 script files, avoid lossy inline encoding paths.

## Usage Rule
- Prefer this skill whenever the task asks to run, debug, or explain Stata empirical pipelines with reproducible outputs.
- Do not use this skill for pure theory discussions with no code/data operations.
