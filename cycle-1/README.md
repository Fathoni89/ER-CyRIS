# ER-CyRIS — Cycle 1 / Research Question 1

Cycle 1 maps operational weaknesses under **specified** datasets, models and stress scenarios. It provides requirements for the later XAI framework; it does not test the current M1–M6 architecture end to end.

- Public benchmark artifacts cover supervised XGBoost and Random Forest plus diagnostic anomaly methods, perturbations, SHAP interpretation and error cases.
- W1–W6 are descriptive findings with domain and configuration boundaries. Noise-related F1 loss and elevated algorithmic alert rate must not be generalized to all conditions or described as measured analyst fatigue.
- The archived metric column `PR_AUC` should be called **Average Precision (AP)** when its producing function is `average_precision_score`. Do not change archived values merely to relabel them.

The [MATRIK article](https://doi.org/10.30812/matrik.v25i3.6147) and JUTIF manuscript (acceptance evidence in the [main README](../README.md)) are prior Cycle 1 outputs. The notebooks and results here remain historical research evidence, including earlier protocol choices. Recheck individual notebook splits and leakage controls before citing a result as a controlled holdout.

Institutional raw logs, response records and credentials do not belong in a public reproduction package.
