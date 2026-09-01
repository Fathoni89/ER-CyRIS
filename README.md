# ER-CyRIS

## Explainable Real-Time Cybersecurity Risk Intelligence System

**ER-CyRIS** is a research framework for explainable and accountable cybersecurity risk intelligence in information-system environments. The framework connects technical cybersecurity evidence with explainability, risk judgment, human oversight, accountable reliance, and organizational learning.

This repository contains the research artifacts, experimental evidence, implementation materials, and publication records supporting the development of ER-CyRIS across three research cycles.

---

## Research Overview

ER-CyRIS is developed through three sequential research cycles:

### Cycle 1 — Technical Evidence and Operational Weakness Mapping

The first cycle investigates the robustness and operational characteristics of machine-learning-based intrusion detection under realistic deployment stressors.

The evaluation uses public cybersecurity datasets and compares supervised and unsupervised approaches under multiple experimental scenarios, including baseline performance, class imbalance, telemetry degradation, drift, parameter sensitivity, and micro-batch inference.

**Main outcome:** identification of operational weaknesses that cannot be adequately captured by benchmark accuracy alone.

### Cycle 2 — Robust and Explainable Log Representation

The second cycle focuses on the construction of a log representation and preprocessing pipeline suitable for cybersecurity risk intelligence in information-system environments.

The cycle investigates the stability, informativeness, and explainability of the resulting representation under noise, missing values, and other realistic data-quality conditions.

**Main outcome:** development and evaluation of the preprocessing/log-representation approach supporting the ER-CyRIS technical pipeline.

### Cycle 3 — Governance Validation and Framework Refinement

The third cycle extends the technical evidence into a governance-oriented mechanism.

The proposed ER-CyRIS architecture connects:

**Technical Evidence → Explainability → Risk Judgment → Human Oversight → Accountable Reliance → Organizational Learning**

Governance expert validation is used to identify agreement, disagreement, operational weaknesses, and opportunities for framework refinement.

The feedback path **M7 → M3** is currently positioned as a **proposed design-level feedback mechanism**. It does not represent automatic pruning, automatic retraining, or closed-loop adaptation unless explicitly demonstrated by an executed experiment.

---

# Research Contribution

The central contribution of ER-CyRIS is not merely the combination of anomaly detection, explainable AI, cybersecurity risk assessment, and governance components.

Instead, ER-CyRIS proposes a mechanism for connecting technical cybersecurity evidence to accountable security decision-making.

The research therefore distinguishes between:

1. **Technical artifact** — the computational mechanisms for producing cybersecurity evidence;
2. **Evidence interpretation** — the use of explainability and contextual information to interpret the evidence;
3. **Risk judgment** — translation of technical evidence into cybersecurity risk considerations;
4. **Human authority and oversight** — mechanisms through which authorized personnel evaluate, accept, escalate, or override system-supported judgments;
5. **Accountable reliance** — conditions under which system outputs can reasonably support organizational decisions; and
6. **Organizational learning** — the use of decision outcomes and expert feedback to inform future refinement.

---

# Publication Record

The research outputs supporting ER-CyRIS are being disseminated through peer-reviewed publications across the research cycles.

| Cycle   | Publication                                                                                                             | Venue                                                                 | Status                                             | Year |
| ------- | ----------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------- | -------------------------------------------------- | ---- |
| Cycle 1 | Operational Weakness Mapping of Machine Learning–Based Intrusion Detection Systems under Realistic Deployment Scenarios | MATRIK: Jurnal Manajemen, Teknik Informatika dan Rekayasa Komputer    | **Published — Sinta 2** | 2026 |
| Cycle 1 | Operational Diagnostics for Intrusion Detection: SHAP-Guided Failure Casebook and SOC Triage Rationale with XGBoost and RandomForest | JUTIF: Jurnal Teknik Informatika | **Accepted / forthcoming October Sinta 2** | 2026 |
| Cycle 2 | Dual View Explainability-aware Log Preprocessing for Robust Anomaly Detection toward ER-CyRIS | International Journal of Electrical and Computer Engineering (IJEECS) | **Accepted — Sinta 1; forthcoming September 2026** | 2026 |

---

# Published Research

## Cycle 1 — MATRIK

**Operational Weakness Mapping of Machine Learning–Based Intrusion Detection Systems under Realistic Deployment Scenarios**

**Authors:**
Fathoni Mahardika, Ema Utami, Kusrini, Ferry Wahyu Wibowo

**Journal:** MATRIK: Jurnal Manajemen, Teknik Informatika dan Rekayasa Komputer

**Indexing:** Sinta 2

**Status:** Published

**DOI:** 10.30812/matrik.v25i3.6147

[View Published Article](https://journal.universitasbumigora.ac.id/matrik/article/view/6147)

This publication constitutes one of the primary research outputs of **Cycle 1** and provides empirical evidence regarding operational weaknesses of machine-learning-based intrusion detection systems under realistic deployment conditions.

---

# Forthcoming Research

## Cycle 1 — JUTIF

**Operational Diagnostics for Intrusion Detection: SHAP-Guided Failure Casebook and SOC Triage Rationale with XGBoost and RandomForest**

A second Cycle 1 publication has been accepted for publication in **JUTIF**, a Sinta 2 journal.

**Status:** Accepted / forthcoming

**Expected publication:** October 2026

The publication extends the Cycle 1 research output and contributes additional evidence to the technical foundation of ER-CyRIS.

> Publication metadata and DOI will be updated in this repository once the article is officially published.

---

## Cycle 2 — IJEECS

**Dual View Explainability-aware Log Preprocessing for Robust Anomaly Detection toward ER-CyRIS**

The Cycle 2 research has been **accepted for publication in the International Journal of Electrical and Computer Engineering (IJEECS)**.

**Journal:** International Journal of Electrical and Computer Engineering (IJEECS)

**Indexing:** Sinta 1

**Status:** Accepted

**Expected publication:** September 2026

The article represents the publication output of **Cycle 2** and supports the development of the technical evidence and log-representation component of ER-CyRIS.

> The final bibliographic metadata, DOI, volume, issue, and publication URL will be updated after official publication.

---

# Research Artifacts

This repository is organized to support reproducibility and traceability of the research process.

### Cycle 1

* Experimental notebooks
* Dataset preprocessing
* Model comparison
* Robustness experiments
* Operational weakness analysis
* Supporting figures and results

### Cycle 2

* Log representation
* Preprocessing pipeline
* Robustness analysis
* Explainability-related experiments
* Supporting results

### Cycle 3

* ER-CyRIS conceptual architecture
* M1–M7 mechanism
* Governance validation materials
* Agreement/disagreement analysis
* Framework refinement
* Supporting dashboard and visualization artifacts

---

# ER-CyRIS Architecture

The conceptual architecture consists of seven major components (M1–M7) connecting technical cybersecurity processing with risk intelligence and governance.

The architecture should be interpreted as a **mechanism**, rather than merely a sequence of computational modules.

The principal conceptual flow is:

```text
Security / System Evidence
          ↓
   Detection & Analysis
          ↓
   Explainable Evidence
          ↓
    Risk Interpretation
          ↓
     Human Judgment
          ↓
 Decision / Escalation / Override
          ↓
   Accountable Reliance
          ↓
 Organizational Learning
```

The proposed **M7 → M3** feedback path represents a design-level mechanism for future refinement. Automatic retraining, pruning, or closed-loop adaptation are outside the demonstrated scope unless explicitly supported by experimental evidence.

---

# Research Transparency

This repository is maintained as a public research companion to the ER-CyRIS research program.

Where appropriate, the repository distinguishes between:

* **Published evidence**
* **Accepted / forthcoming publications**
* **Executed experiments**
* **Conceptual framework components**
* **Proposed mechanisms**
* **Future implementation directions**

This distinction is maintained to avoid overstating the empirical status of research components.

---

# Citation

If you use the research materials or findings from this repository, please cite the corresponding publications listed above.

---

# Researcher

**Fathoni Mahardika**

Doctoral Researcher in Informatics
Universitas Amikom Yogyakarta

Research focus:

* Cybersecurity
* Explainable AI
* Machine Learning
* Cybersecurity Risk Management
* Information Systems Security
* AI Governance
* Accountable AI
* ER-CyRIS

Repository:
https://github.com/Fathoni89/ER-CyRIS
