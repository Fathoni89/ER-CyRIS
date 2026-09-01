# ER-CyRIS Cycle 3 — Institutional Validation and Prototype

Cycle 3 evaluates the integrated ER-CyRIS pipeline on institutional SIUTER/SIAKAD logs and connects technical evidence to explainability, risk translation, operational triage, near-real-time replay, dashboard presentation, and governance validation.

## Primary research artifact

`notebooks/ER_CyRIS_Siklus3_Corrected_Validation_v3_5_Gradio_Fixed2_UI_PUBLIC.ipynb`

This public copy preserves the computational code of the latest v3.5 UI build while removing executed outputs that could expose institution-specific event records or temporary dashboard share URLs.

## Source code

- `src/dashboard_gradio.py` — Gradio/Plotly dashboard source used by the prototype.
- `src/governance_validation_round1.gs` — Governance Expert Validation Round 1 form generator.
- `src/siuter_log_to_dataset_public_template.py` — public-safe adapter template for institutional log preparation; this is intentionally not a verbatim release of the private converter.

## Dashboard

The live Cycle 3 dashboard is maintained separately from the source repository.

**Live dashboard:** https://ercyris-siklus3-v3.fathoni-ee4.workers.dev/

## Governance validation boundary

The public repository does not contain raw institutional logs, expert-response records, or embedded blinded-alert answer keys. The governance validation script is provided as a reproducible instrument definition without publishing respondent data.

## Conceptual boundary

The `M7 → M3` relationship is retained as a **proposed design-level feedback path**. It should not be read as demonstrated automatic pruning, automatic retraining, or closed-loop adaptation.

## Main executed sequence

The corrected notebook implements: leakage/conflict audit; chronological train–calibration–validation–test split; training-only preprocessing and contextual feature augmentation; optional training-only BorderlineSMOTE; XGBoost/Random Forest fitting; calibration and threshold selection; temporal test; Gaussian-noise stress testing; SHAP/FSS; diagnostic analysis; observable-evidence threat inference; provisional NIST-oriented risk mapping with CIA sensitivity analysis; operational triage; expert-validation export; near-real-time benchmark; and dashboard generation.

## Data protection

Sensitive institutional data remain outside this public repository. Derived, non-sensitive research artifacts may be released where appropriate.
