# ER-CyRIS — Cycle 2 / Research Question 2

**Current objective:** design the complete ER-CyRIS explainable AI framework **M1–M6**. This includes implementable input contracts, calculations, rule priorities and unavailable-input outputs for M5 (organizational risk) and M6 (authorized response). Cycle 3 supplies new independently checked cases and organization-specific registers to test those contracts; it is not where M5–M6 are first invented.

## Keep the artifact families separate

| Artifact | Meaning and permissible claim |
| --- | --- |
| [Published IJEECS article](https://doi.org/10.11591/ijeecs.v43.i3.pp871-879), `notebooks/ER_CyRIS_Siklus2_v4_FINAL_fixed.ipynb`, `src/ablation_pipelines.py` and `results/all_results_complete.json` | Historical **M0–M4 preprocessing ablations** and global feature stability under tested configurations. The labels do **not** correspond to architectural modules M1–M4. |
| H1–H5 and file-one M2/M3 technical notebooks | Bounded relationship tests and separate detector/explanation diagnostics; identify the unit, probe and split for each result. |
| Frozen gate comparison and UNSW file-two notebook | Historical margin/SHAP qualification test. In the four reported strata, adding SHAP did not further reduce the accepted set compared with margin only. `q_e` recorded 43-feature completeness and was not a veto. |

A revised source-aware M4 rule and its thresholds must be set during development and tested on **new** cases. The already inspected second UNSW file cannot become its confirmatory holdout after redesign. FSS measured as global top-k overlap does not establish local explanation fidelity.

A separate Cycle 2 framework-design paper is in preparation. The published IJEECS result remains a valid publication about preprocessing and representation within its stated experimental scope; it is not a published validation of the entire M1–M6 chain. M5 requires an audited threat type, time-valid asset, unique approved likelihood scenario, CIA impacts and risk policy, or else returns an explicit noncomputable state. M6 requires a matching approved playbook, authority and approval record; a recommendation is not an executed action.

Original notebooks, numbers and source files remain unchanged as provenance.
