# ER-CyRIS — Explainable and Reliable Cyber-Risk Incident Response

Research repository for the dissertation **“Explainable and Reliable Cyber-Risk Incident Response (ER-CyRIS) untuk Sistem Informasi Organisasi.”** The current research direction is to design an explainable AI framework that connects source-aware evidence, detection, explanation reliability, conditional organizational risk, and authorized incident response. A high detector score or a SHAP attribution is not by itself a verified threat, risk estimate, or permission to act.

## Research sequence and evidence status

| Stage | Work | What the archive supports |
| --- | --- | --- |
| Pre-research | Two systematic literature reviews identify limitations in ML-based security risk management and the use of XAI beyond model interpretation. | Motivation and research gap, not validation of the proposed framework. |
| Cycle 1 / RM1 | Controlled baselines, operational stress tests, SHAP diagnostics, and mapping of W1–W6. | Weaknesses under specified datasets, models, splits and perturbations; W3 is algorithmic alert inflation, not observed analyst fatigue. |
| Cycle 2 / RM2 | Design the **entire M1–M6 framework**, including inputs, rules and failure states for M5 risk translation and M6 governed response. Assess available technical components with bounded experiments. | Design specification and limited technical evidence; organizational risk/response effectiveness remains unproved. |
| Cycle 3 | Test frozen interfaces on independently checked log, threat, asset, policy and action records, when available. | The existing v3.5 notebook/dashboard and its metrics are historical prototype evidence, not automatic validation of the revised M1–M6 chain. |

**Important distinction:** The published IJEECS paper studies dual-view preprocessing, M0–M4 *ablation configurations*, and Feature Stability Score (FSS). Those M0–M4 labels are **not** architectural M1–M4. A separate framework-design paper is being prepared to address the broader Cycle 2 objective; it is not listed as published here.

## Current ER-CyRIS framework (specified in Cycle 2)

| Module | Contract | State of evidence |
| --- | --- | --- |
| **M1 — context and evidence intake** | Keep source, time, observation unit, transformation version and missingness with the log features. | In an earlier UNSW test, `q_e` measured only completeness of 43 features; it did not verify provenance or asset context. |
| **M2 — robust detection** | Use versioned model, preprocessing, threshold and operating condition to produce a candidate alert and detector margin. | Prior model and perturbation experiments are bounded technical evidence. An uncalibrated `predict_proba` score is not organizational incident likelihood. |
| **M3 — explanation reliability** | Record SHAP target/background and local diagnostics with unavailable states. | Global top-k FSS and local diagnostics are different tests. Neither proves explanation fidelity or the correct threat subtype by itself. |
| **M4 — evidence qualification** | Apply separate source, detector and explanation checks; issue `no_alert`, `accept`, `warn` or `abstain` with a reason. | On the earlier second UNSW file, the historical SHAP condition added no exclusion from the accepted set beyond margin-only in the reported strata; `q_e` was logged but not a veto. A revised rule requires new confirmatory data. |
| **M5 — threat-to-risk translation** | Require an independently auditable threat class, time-valid asset, unique approved scenario/likelihood, CIA impacts and versioned risk bands. | Rules and missing-input outcomes are specified in Cycle 2. If inputs fail, return `RISK_NOT_COMPUTABLE` with a reason; no fabricated numeric risk. |
| **M6 — governed response** | Match a valid M5 case to a unique approved playbook; distinguish recommendation, role authorization, actual action and outcome. | Rules are specified in Cycle 2. No approval or policy match means no automatic execution; effectiveness needs independently observed records. |

The unit of analysis moves from **observation → candidate alert → qualified alert → verified threat–asset scenario → recommendation → authorized action**. Examples built from assumed M5/M6 inputs illustrate the calculation but are not measured outcomes.

## Publication status

| Output | Current record | Role in this dissertation |
| --- | --- | --- |
| IEEE ICAISD 2025 and IEEE CITSM 2025 | [SLR 1](https://doi.org/10.1109/ICAISD68166.2025.11385757) · [SLR 2](https://doi.org/10.1109/CITSM67730.2025.11291277) | Research gap. |
| MATRIK 25(3), 2026 | [Published](https://doi.org/10.30812/matrik.v25i3.6147) | Operational weakness mapping, Cycle 1. |
| JUTIF 7(5), 2026 | Accepted / in press per the acceptance record below | SHAP failure casebook and diagnostic rationale, Cycle 1. |
| **IJEECS 43(3), 2026, pp. 871–879** | **[Published; DOI 10.11591/ijeecs.v43.i3.pp871-879](https://doi.org/10.11591/ijeecs.v43.i3.pp871-879)** | Prior preprocessing/representation evidence within Cycle 2; **not** validation of the complete M1–M6 architecture. |
| New Cycle 2 framework-design paper | In preparation | Will present the M1–M6 framework and its bounded evidence; no publication claim. |

## Artifact guide

- [Cycle 1](cycle-1/): notebooks, stress tests, weakness mapping, figures and results.
- [Cycle 2](cycle-2/): published preprocessing ablations plus later technical probes and fixed-protocol gate notebooks. Historical M0–M4 source files remain unchanged to preserve reproducibility.
- [Cycle 3](cycle-3/): historical institutional v3.5 prototype, notebook, derived results, dashboard source and a separate governance instrument.
- [Cycle 3 live dashboard](https://ercyris-siklus3-v3.fathoni-ee4.workers.dev/): presentation of historical prototype outputs; not a claim of full organizational validation.

Some historical material uses the older **M1–M7** labels or an **M7 → M3** feedback arrow. They do not map one-to-one to the current M1–M6 modules, and the arrow does not demonstrate automatic retraining or a closed loop.

Archived columns called `PR_AUC` may contain scikit-learn **Average Precision (AP)**; confirm the producing function in the relevant notebook. Do not silently interpret those figures as trapezoidal area under the precision–recall curve.

## Scope and data handling

Publication of a detector score does not establish attack-class accuracy, organizational risk validity, policy compliance or a successful response. M4's revised marginal benefit must be evaluated on data not used to change its rule; the already examined second UNSW file cannot serve as its independent confirmation. Expert questionnaires, if used, are supplementary governance evidence rather than the primary reference for technical risk/response correctness.

**Release review required:** existing `cycle-3/results/` includes event-level institutional CSV material, although earlier repository text said no such records were public. Preserve controlled originals for research audit and review each public file for identifiers, timestamps, event text and answer-key content before further distribution. Removing a file in a new commit would not erase its prior Git history. No files are deleted by this README update.

## Citation records and original publication details

The records below preserve the paper titles, bibliography and acceptance documentation. IJEECS metadata has been corrected to its published volume, pages and DOI.

# 📑 Publication Records

Full bibliographic records, contribution notes, BibTeX entries, and verbatim transcriptions of the acceptance letters.

**Author team (all outputs):** Fathoni Mahardika (Universitas Sebelas April, Sumedang) · Ema Utami · Kusrini · Ferry Wahyu Wibowo (Universitas Amikom Yogyakarta)
### SLR — First review (IEEE ICAISD 2025)

**Status:** ✅ Published

**Title:** A Systematic Literature Review on Machine Learning-Based Information Security Risk Management for Higher Education Institutions

**Conference:** 2025 IEEE International Conference on Advanced Information Scientific Development (ICAISD)
**Location:** Jakarta, Indonesia
**Publisher:** IEEE
**Date added to IEEE Xplore:** 4 November 2025
**Pages:** 84–89
**Electronic ISBN:** 979-8-3315-7499-4
**DOI:** [10.1109/ICAISD68166.2025.11385757](https://doi.org/10.1109/ICAISD68166.2025.11385757)
**Article URL:** <https://ieeexplore.ieee.org/document/11385757>

**Contribution to ER-CyRIS.** Establishes the contextual gap. From an initial pool of 316
publications, 38 peer-reviewed studies are synthesised and 10 are analysed further on reported
performance. The review maps emerging trends — hybrid machine-learning models, Explainable AI,
and semi-supervised approaches — and shows that work targeting higher-education institutions
specifically remains limited. It proposes the direction that the dissertation then follows: a
scalable, privacy-aware risk-management framework fitted to the constraints of academic
institutions.

**Author keywords:** Systematic Literature Review · Machine Learning · Risk Management ·
Clustering · Explainable AI · Higher Education

#### BibTeX

```bibtex
@inproceedings{mahardika2025slrisrm,
  author    = {Mahardika, Fathoni and Utami, Ema and Kusrini and Wibowo, Ferry Wahyu},
  title     = {A Systematic Literature Review on Machine Learning-Based Information Security Risk Management for Higher Education Institutions},
  booktitle = {2025 IEEE International Conference on Advanced Information Scientific Development (ICAISD)},
  year      = {2025},
  pages     = {84--89},
  address   = {Jakarta, Indonesia},
  publisher = {IEEE},
  doi       = {10.1109/ICAISD68166.2025.11385757},
  isbn      = {979-8-3315-7499-4}
}
```

---

### SLR — Second review (IEEE CITSM 2025)

**Status:** ✅ Published

**Title:** Towards Transparent Cyber Threat Detection: A Systematic Literature Review on the Role of Explainable AI (XAI) in Information Security Risk Management (2018–2025)

**Conference:** 2025 13th International Conference on Cyber and IT Service Management (CITSM)
**Location:** Jakarta, Indonesia
**Publisher:** IEEE
**Date added to IEEE Xplore:** 25 September 2025
**Pages:** 1–4
**Electronic ISBN:** 979-8-3315-7585-4
**DOI:** [10.1109/CITSM67730.2025.11291277](https://doi.org/10.1109/CITSM67730.2025.11291277)
**Article URL:** <https://ieeexplore.ieee.org/document/11291277>

**Contribution to ER-CyRIS.** Establishes the methodological gap. Following PRISMA, the review
examines how Explainable AI is applied within information security risk management and finds a
growing use of SHAP and LIME for interpreting threat-detection models. It also finds that these
techniques are seldom integrated into holistic, real-time risk-management frameworks, especially
in institutional settings such as higher education. That unmet integration is the design problem
ER-CyRIS addresses: carrying explanation forward from model output into risk interpretation,
risk judgment, and accountable human authority.

**Author keywords:** Explainable AI · Systematic Literature Review · Information Security Risk
Management · Cyber Threat Detection · Transparency · SHAP

#### BibTeX

```bibtex
@inproceedings{mahardika2025slrxai,
  author    = {Mahardika, Fathoni and Utami, Ema and Kusrini and Wibowo, Ferry Wahyu},
  title     = {Towards Transparent Cyber Threat Detection: A Systematic Literature Review on the Role of Explainable {AI} ({XAI}) in Information Security Risk Management (2018-2025)},
  booktitle = {2025 13th International Conference on Cyber and IT Service Management (CITSM)},
  year      = {2025},
  pages     = {1--4},
  address   = {Jakarta, Indonesia},
  publisher = {IEEE},
  doi       = {10.1109/CITSM67730.2025.11291277},
  isbn      = {979-8-3315-7585-4}
}
```

---

### Cycle 1 — First output (MATRIK)

**Status:** ✅ Published

**Title:** Operational Weakness Mapping of Machine Learning–Based Intrusion Detection Systems under Realistic Deployment Scenarios

**Journal:** MATRIK: Jurnal Manajemen, Teknik Informatika dan Rekayasa Komputer
**Publisher:** Universitas Bumigora, Mataram, Indonesia
**Accreditation:** Sinta 2
**Volume / Issue:** Vol. 25, No. 3 (July 2026)
**Pages:** 491–508
**DOI:** [10.30812/matrik.v25i3.6147](https://doi.org/10.30812/matrik.v25i3.6147)
**Article URL:** <https://journal.universitasbumigora.ac.id/matrik/article/view/6147>

**Contribution to ER-CyRIS.** Establishes the weakness-mapping evidence that motivates the framework. Supervised detectors (Random Forest, XGBoost) are compared against unsupervised baselines (Isolation Forest, LOF / kNN-distance, DBSCAN) across four public datasets — CICIDS2017, CICIDS2018, UNSW-NB15, and RanSMAP — under realistic deployment perturbations. The article reports near-perfect baseline performance that degrades sharply under minor Gaussian noise, and argues that evaluation must extend beyond accuracy benchmarking to robustness, interpretability, and alert management. This finding is the empirical basis for treating the detector as a producer of evidence rather than as a decision authority.

**Mapped repository artifacts:** [`cycle-1/`](cycle-1/)

#### BibTeX

```bibtex
@article{mahardika2026weakness,
  author  = {Mahardika, Fathoni and Utami, Ema and Kusrini and Wibowo, Ferry Wahyu},
  title   = {Operational Weakness Mapping of Machine Learning--Based Intrusion
             Detection Systems under Realistic Deployment Scenarios},
  journal = {MATRIK: Jurnal Manajemen, Teknik Informatika dan Rekayasa Komputer},
  volume  = {25},
  number  = {3},
  pages   = {491--508},
  year    = {2026},
  doi     = {10.30812/matrik.v25i3.6147},
  url     = {https://journal.universitasbumigora.ac.id/matrik/article/view/6147}
}
```

---

### Cycle 1 — Second output (JUTIF)

**Status:** 🕓 Accepted — scheduled for publication

**Title:** Operational Diagnostics for Intrusion Detection: SHAP-Guided Failure Casebook and SOC Triage Rationale with XGBoost and RandomForest

**Journal:** JUTIF — Jurnal Teknik Informatika
**Publisher:** Universitas Jenderal Soedirman (UNSOED), Purbalingga, Indonesia
**Accreditation:** Sinta 2 — Decree of the Director General of Higher Education, Research, and Technology No. 177/E/KPT/2024
**P-ISSN:** 2723-3863 · **E-ISSN:** 2723-3871
**Scheduled issue:** Volume 7, Number 5 — October 2026
**Letter of Acceptance:** No. 5711/LoA/JUTIF/II/2026, dated 24 February 2026
**Signed by:** Dr. Ir. Lasmedi Afuan, S.T., M.Cs., IPM. (Chief Editor)
**Journal URL:** <http://jutif.if.unsoed.ac.id>

**Contribution to ER-CyRIS.** Develops the SHAP-guided failure casebook and the SOC triage rationale. Where the MATRIK article establishes *that* detectors fail under realistic conditions, this article establishes *how those failures can be read* — turning model errors into diagnosable, explainable cases that a security analyst can act on. It supplies the explainability layer of the framework.

**Mapped repository artifacts:** [`cycle-1/`](cycle-1/)

#### BibTeX

```bibtex
@article{mahardika2026diagnostics,
  author  = {Mahardika, Fathoni and Utami, Ema and Kusrini and Wibowo, Ferry Wahyu},
  title   = {Operational Diagnostics for Intrusion Detection: {SHAP}-Guided Failure
             Casebook and {SOC} Triage Rationale with {XGBoost} and {RandomForest}},
  journal = {JUTIF: Jurnal Teknik Informatika},
  volume  = {7},
  number  = {5},
  year    = {2026},
  note    = {In press. Accepted 24 February 2026, LoA No. 5711/LoA/JUTIF/II/2026},
  issn    = {2723-3871}
}
```

---

### Cycle 2 (IJEECS)

**Status:** ✅ Published — Vol. 43, No. 3, 2026, pp. 871–879

**Title:** Dual View Explainability-aware Log Preprocessing for Robust Anomaly Detection toward ER-CyRIS

**Journal:** IJEECS — Indonesian Journal of Electrical Engineering and Computer Science
**Publisher:** Institute of Advanced Engineering and Science (IAES)
**Indexing:** Check current SINTA and Scopus records separately; publication is documented at the journal article page.
**P-ISSN:** 2502-4752 · **E-ISSN:** 2502-4760
**Paper ID:** #46518
**Acceptance date:** 19 August 2026
**Published in:** Vol. 43, No. 3 (2026), pp. 871–879
**DOI:** [10.11591/ijeecs.v43.i3.pp871-879](https://doi.org/10.11591/ijeecs.v43.i3.pp871-879)
**Article URL:** <https://ijeecs.iaescore.com/index.php/IJEECS/article/view/46518>

**Contribution to ER-CyRIS.** Presents the dual-view (Semantic View + Contextual Deviation View) log preprocessing pipeline, the M0–M4 ablation across four datasets, and the Feature Stability Score (FSS) as a diagnostic stability criterion. Its M0–M4 names are experimental preprocessing configurations, not the architectural M1–M4 defined in the subsequent framework design. FSS measures selected global feature-set overlap; it does not by itself establish local explanation fidelity or effectiveness of the complete framework.

**Mapped repository artifacts:** [`cycle-2/`](cycle-2/)

#### BibTeX

```bibtex
@article{mahardika2026dualview,
  author  = {Mahardika, Fathoni and Utami, Ema and Kusrini and Wibowo, Ferry Wahyu},
  title   = {Dual View Explainability-aware Log Preprocessing for Robust Anomaly
             Detection toward {ER-CyRIS}},
  journal = {Indonesian Journal of Electrical Engineering and Computer Science},
  year    = {2026},
  volume  = {43},
  number  = {3},
  pages   = {871--879},
  doi     = {10.11591/ijeecs.v43.i3.pp871-879},
  url     = {https://ijeecs.iaescore.com/index.php/IJEECS/article/view/46518},
  issn    = {2502-4760}
}
```

---

### Cycle 3 — In preparation

Cycle 3 contains an institutional prototype, scenario-oriented risk mapping, near-real-time benchmarking, and a separate governance instrument. These historical artifacts do not alone validate every interface of the current M1–M6 architecture, the revised M4 gate, or organizational risk and response effectiveness.

Manuscript preparation is in progress. This section will be updated when a submission or acceptance record exists.

---

### How the publications map to the framework layers

| ER-CyRIS layer | Established by | Venue |
| :------------- | :------------- | :---- |
| Research gap — ML-based ISRM in higher education is under-served | SLR, first review | IEEE ICAISD 2025 |
| Research gap — explanation rarely reaches real-time risk decisions | SLR, second review | IEEE CITSM 2025 |
| Problem evidence — detector fragility under realistic conditions | Cycle 1, first output | MATRIK |
| Explainability — failure casebook and triage rationale | Cycle 1, second output | JUTIF |
| Prior evidence — dual-view preprocessing and global feature-set stability diagnostics | Cycle 2 | IJEECS (published, 2026) |
| M1–M6 architecture — interface and rule specification, including M5–M6 | Cycle 2 framework-design manuscript | In preparation; distinct from IJEECS |
| Conditional framework evaluation with independently checked organizational records | Cycle 3 | Current prototype evidence is bounded; complete validation not established |
---

### Verification

* the DOI resolvers for the three published outputs:
  <https://doi.org/10.1109/ICAISD68166.2025.11385757>,
  <https://doi.org/10.1109/CITSM67730.2025.11291277>, and
  <https://doi.org/10.30812/matrik.v25i3.6147>, and
  <https://doi.org/10.11591/ijeecs.v43.i3.pp871-879>;
* the IEEE Xplore record pages: <https://ieeexplore.ieee.org/document/11385757> and
  <https://ieeexplore.ieee.org/document/11291277>;
* the journal article page: <https://journal.universitasbumigora.ac.id/matrik/article/view/6147>;

Accepted-but-unpublished items are marked as such throughout this repository, and no claim of publication is made for them until the corresponding issue is released.

---

## 📄 Acceptance Letter Transcriptions

### Transcription — IJEECS acceptance notice

Provided as a text record alongside the source file.

> **Paper ID# 46518**
>
> Dear Prof/Dr/Mr/Mrs: Fathoni Mahardika,
>
> It is my great pleasure to inform you that your paper entitled *"Dual View Explainability-aware Log Preprocessing for Robust Anomaly Detection toward ER-CyRIS"* is ACCEPTED and will be published on the Indonesian Journal of Electrical Engineering and Computer Science later, after all final documents have been completed and reached us.
>
> Your paper will be scheduled for publication in an upcoming issue (tentatively the September 2026 issue) of the journal.
>
> Best Regards,
> Prof. Dr. Ir. Tole Sutikno, Editor, IJEECS

Received 19 August 2026 from the IJEECS editorial office.

---

### Transcription — JUTIF Letter of Acceptance

> **No. 5711/LoA/JUTIF/II/2026** — Letter of Acceptance, 24 February 2026
>
> Jurnal Teknik Informatika (JUTIF), Universitas Jenderal Soedirman.
> P-ISSN 2723-3863, E-ISSN 2723-3871. Accredited SINTA 2 based on Decree No. 177/E/KPT/2024.
>
> Title: *Operational Diagnostics for Intrusion Detection: SHAP-Guided Failure Casebook and SOC Triage Rationale with XGBoost and RandomForest*
>
> Authors: Fathoni Mahardika (Universitas Sebelas April), Ema Utami (Universitas Amikom Yogyakarta), Kusrini (Universitas Amikom Yogyakarta), Ferry Wahyu Wibowo (Universitas Amikom Yogyakarta)
>
> Based on the review results, the article is ACCEPTED for publication in JUTIF, Volume 7 Number 5, October 2026.
>
> Chief Editor: Dr. Ir. Lasmedi Afuan, S.T., M.Cs., IPM.

---

## License and Use

The repository is intended primarily for academic research, transparency, and reproducibility.

Users should cite the corresponding publications and dissertation when using or discussing the research artifacts.
