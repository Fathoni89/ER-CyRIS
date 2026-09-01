# ER-CyRIS Cycle 2 — Robust and Explainable Log Preprocessing

This directory contains the public research artifacts for Cycle 2. The cycle evaluates preprocessing and representation configurations through ablation, robustness testing, and SHAP/FSS analysis.

## Primary research artifact

- `notebooks/ER_CyRIS_Siklus2_v4_FINAL_fixed.ipynb` — executed final notebook used for the Cycle 2 experiments.

## Source code

- `src/ablation_pipelines.py` — M0–M4 experimental preprocessing/augmentation classes extracted from the final notebook.
- `src/evaluation_helpers.py` — evaluation and result-saving helpers extracted from the final notebook.

## Research boundary

Cycle 2 is the preprocessing/representation layer. XGBoost and Random Forest are evaluation instruments, and FSS is used as a diagnostic explanation-stability criterion. Full institutional ER-CyRIS validation, NIST-oriented risk translation, dashboarding, and governance assessment belong to Cycle 3.

## Datasets

The notebook uses public cybersecurity benchmark datasets. Dataset binaries are not redistributed in this repository; use the original dataset sources referenced in the notebook/paper.
