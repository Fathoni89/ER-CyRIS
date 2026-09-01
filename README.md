# ER-CyRIS — Explainable Real-Time Cybersecurity Risk Intelligence

**ER-CyRIS** is a research framework developed in a doctoral dissertation on real-time cyber threat detection and explainable cybersecurity risk intelligence for academic information systems.

The repository provides the computational artifacts, experimental notebooks, source code, dashboard prototype, and supporting documentation developed across three research cycles.

The central research argument of ER-CyRIS is not limited to anomaly detection or explainable machine learning. ER-CyRIS is designed to connect:

**Technical Evidence → Explainability → Risk Interpretation → Risk Judgment → Human Authority → Accountable Reliance → Organizational Learning**

This repository therefore distinguishes clearly between **implemented computational artifacts**, **empirical evidence**, and **conceptual/proposed mechanisms**.

---

## 🎯 Research Objective

The research aims to develop and evaluate an explainability-aware cybersecurity risk intelligence framework that can support the translation of technical detection evidence into accountable cybersecurity risk decisions.

The research focuses on maintaining a clear relationship between:

* cybersecurity detection;
* evidence generation;
* explainable interpretation;
* cybersecurity risk assessment;
* operational triage;
* human oversight;
* governance and accountability; and
* organizational learning.

---

# 🔬 Research Cycles

## Cycle 1 — Technical Detection and Robustness

Cycle 1 establishes the technical foundation of ER-CyRIS through experiments using public cybersecurity datasets.

The cycle focuses on:

* anomaly and intrusion detection;
* comparative evaluation of machine-learning approaches;
* preprocessing and feature preparation;
* model performance evaluation;
* robustness analysis under noise and missing values; and
* identification of the technical evidence required by subsequent ER-CyRIS stages.

The resulting evidence provides the technical foundation for the development of the subsequent research cycles.

### Main artifacts

* Experimental notebooks
* Model evaluation results
* Robustness experiments
* Supporting figures and results
* Research documentation

---

## Cycle 2 — Log Representation and Stability

Cycle 2 focuses on the development and evaluation of a log-representation and preprocessing pipeline for academic information-system security logs.

The cycle investigates how operational logs can be transformed into representations that remain:

* informative;
* stable;
* robust to missing or noisy observations; and
* suitable for subsequent explainability and risk-oriented analysis.

The cycle includes the **M0–M4 ablation experiment** and the use of the **Feature Stability Score (FSS)** as a diagnostic stability criterion.

The main methodological components include:

* log preprocessing;
* missing-value handling;
* feature transformation;
* token/feature preservation;
* ablation analysis;
* stability diagnostics; and
* evaluation of representation quality.

### Main artifacts

* Final Cycle 2 experimental notebook
* M0–M4 ablation source modules
* Evaluation utilities
* Experimental results
* Figures and supporting documentation
* Python environment requirements

---

## Cycle 3 — ER-CyRIS Integration and Governance Validation

Cycle 3 integrates the technical evidence developed in the previous cycles into the ER-CyRIS research prototype.

The cycle focuses on the relationship between:

**Evidence → Explainability → Risk Judgment → Human Oversight → Accountable Reliance**

The prototype includes computational components for:

* cybersecurity detection;
* explainability;
* SHAP-based interpretation;
* operational triage;
* cybersecurity risk mapping;
* NIST-oriented risk interpretation;
* near-real-time performance benchmarking; and
* governance-oriented validation.

The Cycle 3 dashboard provides an interactive representation of the implemented prototype and its analytical outputs.

### Main artifacts

* Corrected Cycle 3 research notebook
* Dashboard source code
* Governance expert-validation instrument
* Framework-refinement documentation
* Experimental results
* Supporting figures
* Python environment requirements

---

# 🚀 Cycle 3 Live Dashboard

The Cycle 3 dashboard provides an interactive view of the implemented ER-CyRIS prototype.

It is intended to demonstrate how technical outputs can be presented as evidence for explainability, operational triage, and cybersecurity risk interpretation.

**Live Dashboard:**
[Open the ER-CyRIS Cycle 3 Dashboard](dashboard/cycle-3/DASHBOARD_URL.txt)

The dashboard includes research-oriented views covering:

* Overview
* Detection Metrics
* SHAP Explainability
* Triage Rationale
* NIST Risk Mapping
* Near-Real-Time Performance

A persistent dashboard URL is maintained in:

`dashboard/cycle-3/DASHBOARD_URL.txt`

---

# 📂 Repository Structure

```text
ER-CyRIS/
│
├── cycle-1/
│   ├── notebooks/
│   ├── src/
│   ├── results/
│   ├── figures/
│   └── environment/
│
├── cycle-2/
│   ├── notebooks/
│   ├── src/
│   ├── results/
│   ├── figures/
│   └── requirements.txt
│
├── cycle-3/
│   ├── notebooks/
│   ├── src/
│   ├── governance-validation/
│   ├── framework-refinement/
│   ├── results/
│   ├── figures/
│   └── requirements.txt
│
├── dashboard/
│   └── cycle-3/
│       ├── README.md
│       └── DASHBOARD_URL.txt
│
├── docs/
│   └── PUBLIC_DATA_BOUNDARY.md
│
└── README.md
```

---

# 🧪 Research Artifacts

| Research Cycle | Artifact                         | Repository Location                                                                          |
| -------------- | -------------------------------- | -------------------------------------------------------------------------------------------- |
| Cycle 1        | Experimental notebooks           | [`cycle-1/notebooks/`](cycle-1/notebooks/)                                                   |
| Cycle 1        | Results and figures              | [`cycle-1/results/`](cycle-1/results/)                                                       |
| Cycle 2        | Final experimental notebook      | [`cycle-2/notebooks/`](cycle-2/notebooks/)                                                   |
| Cycle 2        | M0–M4 ablation modules           | [`cycle-2/src/`](cycle-2/src/)                                                               |
| Cycle 2        | Evaluation utilities             | [`cycle-2/src/`](cycle-2/src/)                                                               |
| Cycle 3        | Corrected research notebook      | [`cycle-3/notebooks/`](cycle-3/notebooks/)                                                   |
| Cycle 3        | Dashboard source                 | [`cycle-3/src/dashboard_gradio.py`](cycle-3/src/dashboard_gradio.py)                         |
| Cycle 3        | Governance validation instrument | [`cycle-3/src/governance_validation_round1.gs`](cycle-3/src/governance_validation_round1.gs) |
| Cycle 3        | Framework refinement             | [`cycle-3/framework-refinement/`](cycle-3/framework-refinement/)                             |
| Cycle 3        | Live dashboard                   | [`dashboard/cycle-3/`](dashboard/cycle-3/)                                                   |

---

# 🧩 ER-CyRIS Mechanism

The ER-CyRIS framework is organized around a hierarchical mechanism rather than a collection of independent technical components.

The intended relationship is:

```text
Technical Artifact
       ↓
Cybersecurity Evidence
       ↓
Explainable Interpretation
       ↓
Risk Judgment
       ↓
Human Authority / Oversight
       ↓
Accountable Reliance
       ↓
Organizational Learning
```

Accordingly, the technical model is treated as a producer of evidence rather than as the final decision authority.

The framework distinguishes between:

1. **technical evidence generation**;
2. **interpretation of evidence**;
3. **risk judgment**;
4. **human decision authority**;
5. **accountability mechanisms**; and
6. **organizational learning**.

This distinction is central to the scientific argument of ER-CyRIS.

---

# 🔄 M7 → M3 Feedback Boundary

The relationship between **M7 and M3** is retained as a:

> **Proposed Design-Level Feedback Path**

This relationship represents a conceptual mechanism for using governance and operational feedback to inform subsequent refinement of the technical pipeline.

The current research does **not** claim that the prototype has demonstrated:

* automatic pruning;
* automatic retraining;
* autonomous model adaptation;
* closed-loop adaptation; or
* fully automated governance feedback.

These mechanisms remain future implementation and validation directions unless explicitly supported by executed experiments.

This boundary is maintained to distinguish the **implemented prototype** from the **proposed framework mechanism**.

---

# 👥 Governance Expert Validation

Technical validation and governance expert validation are treated as two different forms of evidence.

### Technical Validation

Technical validation evaluates whether the computational system can produce technically meaningful evidence, alerts, explanations, and performance measurements.

### Governance Expert Validation

Governance expert validation evaluates whether the proposed mechanisms for:

* evidence interpretation;
* risk judgment;
* escalation;
* human oversight;
* override;
* accountable reliance; and
* organizational learning

are considered reasonable and acceptable by relevant experts.

The governance validation is therefore not interpreted simply as a percentage of agreement.

Disagreement is treated as potentially valuable evidence for framework refinement.

The intended refinement process is:

```text
Initial ER-CyRIS
       ↓
Expert Validation
       ↓
Agreement / Disagreement Analysis
       ↓
Identification of Weaknesses
       ↓
Framework Refinement
       ↓
Refined ER-CyRIS
```

---

# 🔐 Data Availability and Research Boundary

This repository is designed to provide reproducible computational artifacts while respecting data confidentiality.

Publicly shareable code, notebooks, documentation, and research artifacts may be included in the repository.

Institutional security logs, identifiable academic-system records, expert-response datasets, credentials, API keys, and other sensitive materials are not publicly released.

Where sensitive data are required to execute a particular experiment, the repository provides the corresponding computational logic or documentation without exposing the underlying confidential data.

See:

[`docs/PUBLIC_DATA_BOUNDARY.md`](docs/PUBLIC_DATA_BOUNDARY.md)

---

# 📊 Reproducibility

The repository provides:

* research notebooks;
* source-code modules;
* evaluation utilities;
* environment requirements;
* dashboard source;
* validation instruments;
* research documentation; and
* supporting results.

The notebooks document the computational workflow used during the corresponding research cycle.

Exact reproduction of experiments involving institutional data may require access to the original controlled datasets and research environment.

---

# 📚 Publications

The repository also documents the research outputs associated with the three research cycles.

### Cycle 1

* Published research output in **MATRIK — Jurnal Manajemen, Teknik Informatika dan Rekayasa Komputer**, Sinta 2.
**Operational Weakness Mapping of Machine Learning–Based Intrusion Detection Systems under Realistic Deployment Scenarios**
**https://journal.universitasbumigora.ac.id/matrik/article/view/6147**
* A second Cycle 1 manuscript has been accepted and is scheduled for publication On October 2026.
**JUTIF — Jurnal Teknik Informatika, UNSOED**, Sinta 2.
**Operational Diagnostics for Intrusion Detection: SHAP-Guided Failure Casebook and SOC Triage Rationale with XGBoost and RandomForest**

### Cycle 2

* Research output accepted for publication in **IJEECS — Indonesian Journal of Electrical Engineering and Computer Science**, Sinta 1.
**Dual View Explainability-aware Log Preprocessing for Robust Anomaly Detection toward ER-CyRIS**


Publication information and links are maintained in the corresponding repository documentation.

---

# ⚖️ Scientific Scope

ER-CyRIS should not be interpreted as a claim that machine-learning predictions independently determine cybersecurity risk decisions.

The framework instead investigates how technical evidence and explainable outputs can be incorporated into a broader mechanism in which authorized human actors retain responsibility for risk judgment and consequential decisions.

The scientific contribution therefore lies in the mechanism connecting:

**technical evidence → interpretation → risk judgment → accountable human reliance**

rather than in the accumulation of independent machine-learning components.

---

# 🎓 Dissertation Research Context

ER-CyRIS is developed as part of doctoral research in Informatics with a focus on cybersecurity, explainable machine learning, digital transformation engineering, and accountable cybersecurity risk intelligence.

The repository serves as a supporting research artifact and evidence trail for the dissertation.

---

## License and Use

The repository is intended primarily for academic research, transparency, and reproducibility.

Users should cite the corresponding publications and dissertation when using or discussing the research artifacts.
