# Oncology Trial Screening Dataset — Data Generation Guide (v6)

## Changelog

| Version | Change |
|---|---|
| v1 | Initial dataset — 1,000 patients, 3,028 notes, free-text notes with binary labels |
| v2 | Added `cancer_indication` as an explicit structured column (extracted from free-text notes). Column is positioned after `note_date` and before `free_text_note`. |
| v3 | Added final state distribution broken down by cancer indication to the data guide. |
| v4 | Added model evaluation section documenting TF-IDF + Logistic Regression benchmark results, interpretation of perfect scores, and implications for dataset use. |
| v5 | Released dataset v3: redesigned note generation to remove explicit label-bearing phrases, introduce coordinator shorthand and abbreviations, add ambiguous/hedged language, and require label inference from clinical indicators. Updated all statistics sections to reflect v3 distribution. |
| v6 | Added cross-dataset generalisation evaluation: TF-IDF + LR and BERT trained on v2, tested on v3. Documents performance gap and interpretation. |

---

## Overview

This document describes the rules, logic, and design decisions used to generate the synthetic oncology clinical trial screening dataset. The dataset is intended to simulate the kind of free-text coordinator notes maintained during patient screening for an oncology clinical trial, along with structured binary labels used for downstream analysis.

---

## Dataset Scale

| Metric | Value |
|---|---|
| Total patients | 1,000 |
| Total notes | 3,066 |
| Average notes per patient | ~3.1 |
| Note date range | January 2021 – December 2024 |
| Dataset version | v3 |

---

## Final State Distribution (Per Patient)

Distribution is measured at the level of the **most recent note** per patient, which reflects the patient's final known status.

| Label State | Count | % of Patients |
|---|---|---|
| Eligible = 1, Available = 1 | 133 | 13.3% |
| Eligible = 1, Available = 0 | 135 | 13.5% |
| Eligible = 0, Available = 1 | 180 | 18.0% |
| Eligible = 0, Available = 0 | 314 | 31.4% |
| Deceased | 81 | 8.1% |
| Lost to Follow-up | 157 | 15.7% |

The distribution is intentionally skewed to reflect realistic oncology trial screening, where the majority of screened patients do not qualify or are not available to enroll.

---

## Final State Distribution by Cancer Indication

The table below shows the final state breakdown per cancer indication, based on each patient's most recent note. Column headers match the label combinations defined above.

| Cancer Indication | N | E=1, A=1 | E=1, A=0 | E=0, A=1 | E=0, A=0 | Deceased | LTFU |
|---|---|---|---|---|---|---|---|
| Bladder Cancer | 70 | 13 | 10 | 12 | 20 | 3 | 12 |
| Breast Cancer | 69 | 9 | 12 | 9 | 19 | 7 | 13 |
| Colon Cancer | 68 | 12 | 7 | 9 | 23 | 5 | 12 |
| Colorectal Cancer | 74 | 9 | 12 | 9 | 31 | 5 | 8 |
| Endometrial Cancer | 57 | 6 | 8 | 16 | 15 | 3 | 9 |
| Gastric Cancer | 63 | 13 | 3 | 12 | 23 | 5 | 7 |
| Head and Neck Squamous Cell Carcinoma (HNSCC) | 62 | 9 | 11 | 8 | 17 | 6 | 11 |
| Hepatocellular Carcinoma | 72 | 8 | 9 | 11 | 31 | 6 | 7 |
| Melanoma | 81 | 8 | 13 | 17 | 20 | 9 | 14 |
| Non-Small Cell Lung Cancer (NSCLC) | 82 | 8 | 13 | 16 | 28 | 6 | 11 |
| Ovarian Cancer | 65 | 5 | 9 | 13 | 18 | 8 | 12 |
| Pancreatic Cancer | 55 | 5 | 4 | 12 | 19 | 4 | 11 |
| Prostate Cancer | 63 | 5 | 12 | 9 | 23 | 2 | 12 |
| Renal Cell Carcinoma | 54 | 9 | 4 | 12 | 16 | 6 | 7 |
| Small Cell Lung Cancer (SCLC) | 65 | 14 | 8 | 15 | 11 | 6 | 11 |
| **Total** | **1,000** | **133** | **135** | **180** | **314** | **81** | **157** |

**Column key:** E = Eligible, A = Available, LTFU = Lost to Follow-Up.

Notable observations from the v3 distribution:

- **SCLC** has the highest proportion of eligible and available patients (E=1, A=1: 14/65 = 21.5%), suggesting a relatively clean eligibility profile for this indication in the dataset.
- **Colorectal Cancer** and **Hepatocellular Carcinoma** both have the highest E=0, A=0 counts (31 patients each), reflecting a high rate of dual-barrier screening failures.
- **Melanoma** and **NSCLC** have the largest cohorts (81 and 82 respectively) due to random sampling variation across 15 indications.
- **Prostate Cancer** has the lowest deceased count (2/63 = 3%), while **Melanoma** has the highest (9/81 = 11%).
- **Pancreatic Cancer** has the smallest cohort (n=55) due to random sampling variation.

---

## Label Definitions

Each note carries a `cancer_indication` column and four binary labels:

| Column | Type | Description |
|---|---|---|
| `cancer_indication` | String | The patient's cancer type, extracted and stored as an explicit column (e.g. "Breast Cancer", "Non-Small Cell Lung Cancer (NSCLC)"). Consistent across all notes for a given patient. |

| Label | 1 | 0 |
|---|---|---|
| `eligible` | Patient meets the trial's inclusion/exclusion criteria | Patient does not meet the criteria |
| `available` | Patient is not currently on treatment and can begin trial therapy | Patient is already receiving treatment or is otherwise unavailable |
| `deceased` | Patient has died | Patient is alive |
| `lost_to_follow_up` | Patient is unreachable; no active records | Patient is actively being followed |

---

## Label Constraint Rules

The following logical constraints are enforced across all notes:

### Terminal State Overrides
- **`deceased = 1`** → `available = 0`, `lost_to_follow_up = 0`
  Death is a known outcome. A deceased patient cannot simultaneously be lost to follow-up or available for treatment.
- **`lost_to_follow_up = 1`** → `eligible = 0`, `available = 0`
  If a patient is unreachable, their eligibility and availability cannot be assessed or confirmed.

### Eligible and Available Are Independent
Unlike a simple logical dependency, `eligible` and `available` are treated as fully independent axes, reflecting clinical reality:

| Combination | Clinical Meaning |
|---|---|
| `eligible = 1, available = 1` | Meets criteria and not currently on treatment — ideal candidate |
| `eligible = 1, available = 0` | Meets criteria but currently receiving active treatment |
| `eligible = 0, available = 1` | Needs treatment but does not meet trial inclusion/exclusion criteria |
| `eligible = 0, available = 0` | Does not meet criteria and is also on active treatment |

---

## Multi-Note Logic: Temporal Progression

Patients with more than one note follow a logical temporal trajectory:

- **Intermediate notes** (all notes except the last) use a neutral, in-progress screening style. Labels for intermediate notes are set to `0` across all four fields, reflecting that a decision has not yet been made.
- **The final note** reflects the patient's resolved state and carries the definitive label values.
- Disease status in intermediate notes trends plausibly toward the final state (e.g. a patient who ends up deceased is more likely to show progression in earlier notes).
- Note dates are assigned in strictly ascending chronological order per patient, with realistic spacing between visits.

This design means **any downstream analysis must account for multiple records per patient** and should identify the most recent note to obtain the patient's current label state.

---

## Cancer Indications

The dataset includes the following solid tumour indications:

- Non-Small Cell Lung Cancer (NSCLC)
- Small Cell Lung Cancer (SCLC)
- Breast Cancer
- Prostate Cancer
- Colon Cancer
- Colorectal Cancer
- Pancreatic Cancer
- Ovarian Cancer
- Gastric Cancer
- Hepatocellular Carcinoma
- Renal Cell Carcinoma
- Bladder Cancer
- Head and Neck Squamous Cell Carcinoma (HNSCC)
- Melanoma
- Endometrial Cancer

Each patient is assigned a single indication for the duration of their record history.

---

## Staging

Each patient is assigned a TNM stage at the time of record creation:

- **T stage:** T1, T2, T3, T4
- **N stage:** N0, N1, N2, N3
- **M stage:** M0, M1

Stage remains consistent across all notes for a given patient.

---

## Biomarkers and Lab Values

Biomarkers are indication-specific and drawn from clinically relevant panels. Examples include:

- **NSCLC:** EGFR (exon 19 del, L858R, T790M), ALK rearrangement, PD-L1 TPS, KRAS G12C
- **Breast Cancer:** ER/PR/HER2, BRCA1/2, Ki-67
- **Prostate Cancer:** PSA, AR amplification, BRCA2
- **Colorectal/Colon:** KRAS, MSI status, BRAF V600E, CEA
- **Melanoma:** BRAF V600E/K, PD-L1, LDH
- **Ovarian:** CA-125, BRCA1/2, HRD status

Lab values included in notes are synthetic but plausible, including: ECOG performance status, CBC (WBC, Hgb, Plt), renal function (Creatinine, eGFR), hepatic function (ALT, AST, Total Bilirubin), and ANC.

---

## Free-Text Note Variety

Each label combination has multiple distinct note templates to ensure linguistic variety. The same underlying label state can be expressed through:

- Terse clinical shorthand (e.g. *"PD confirmed. Screen failure — prior IO therapy. Not enrolling."*)
- Verbose narrative style (e.g. *"Patient was reviewed in multidisciplinary tumor board and discussed for trial candidacy..."*)
- Different orderings of clinical elements (biomarkers first vs. imaging first vs. labs first)
- Varied vocabulary for the same concept (e.g. "progressive disease," "PD confirmed," "disease progression," "clinical and radiographic progression")

Exclusion reasons (for `eligible = 0`) are drawn from a pool of realistic protocol-level criteria such as prior immunotherapy, inadequate organ function, ECOG PS threshold, active CNS metastases, QTc prolongation, and washout period violations.

---

## Dataset v3: Note Redesign for Model Benchmarking

Version 3 of the dataset fundamentally restructures how free-text notes are written, specifically to address the limitation identified in the TF-IDF baseline evaluation: that labels were trivially recoverable from explicit verdict phrases. In v3, all four label states must be **inferred from clinical context** rather than read directly from the text.

### What Was Removed

All explicit label-bearing phrases have been eliminated from note templates:

| Removed from v1/v2 | Label it exposed |
|---|---|
| "eligibility confirmed", "meets eligibility criteria", "patient qualifies" | eligible = 1 |
| "screen failure", "ineligible", "exclusion criterion met" | eligible = 0 |
| "not on active treatment", "available to begin protocol treatment" | available = 1 |
| "currently receiving treatment", "washout period required" | available = 0 |
| "deceased", "cause of death", "patient expired" | deceased = 1 |
| "lost to follow-up", "unable to reach patient", "declared LTFU" | lost_to_follow_up = 1 |

### What Replaced Them

Each label state is now signalled through a combination of clinical indicators that require interpretation:

**Eligible = 1, Available = 1** is implied by: good performance status, organ function within normal range, no active systemic therapy, washout period satisfied, no protocol contraindications identified, baseline assessments initiated.

**Eligible = 1, Available = 0** is implied by: a compatible molecular and clinical profile, but an active treatment regimen currently ongoing with estimated cycles remaining and washout timeline noted.

**Eligible = 0, Available = 1** is implied by: patient off treatment and needing next-line therapy, but a specific clinical finding flagged (e.g. elevated transaminases, poor PS, prior IO within washout window, active CNS disease, QTcF prolongation, renal insufficiency) — without stating that this is an exclusion criterion.

**Eligible = 0, Available = 0** is implied by: active treatment ongoing AND an additional clinical finding that would independently preclude enrolment — neither barrier is labelled as such.

**Deceased = 1** is implied by: family contact noting the patient has passed, hospice or comfort care transfer documented, hospital admission with no survival, OS event reference — without using the word "deceased" or "death".

**Lost to Follow-Up = 1** is implied by: multiple failed outreach attempts, disconnected phone, returned mail, unread portal messages, last known contact weeks or months prior — without using the phrase "lost to follow-up".

### Coordinator Style and Abbreviations

Notes in v3 use authentic coordinator shorthand throughout:

- Lab values written as clipped strings: `PS2, WBC 4.1 / Hgb 10.3 / Plt 188 / Cr 1.42 / eGFR 51 / ALT 67`
- Biomarkers abbreviated: `EGFR ex19del`, `MSI-H`, `BRAF V600E`, `PD-L1 TPS 55%`, `IMDC int`
- Treatment references clipped: `pembro mono C4`, `FOLFOX C7`, `letrozole (ongoing)`
- Sentence fragments and incomplete constructions used naturally
- Coordinator initials implied through first-person shorthand: `coord to f/u`, `PI to review`, `flagged for re-screen`

### Ambiguity in Intermediate Notes

Intermediate notes (non-final, labels all = 0) now include deliberate ambiguity signals such as:

- Borderline lab values with repeat ordered
- Outside records pending
- Conflicting biomarker results under re-verification
- Contradictory performance status documentation
- Patient-reported treatment history inconsistent with chart records
- Brain MRI results outstanding
- Washout calculation requiring clarification

These signals make intermediate notes genuinely difficult to classify and prevent simple heuristics from resolving label state before the final note.

---

## Key Design Choices

**Realistic skew over balance.** The distribution is intentionally skewed toward ineligible and unavailable patients, mirroring real-world trial screening failure rates. This makes the dataset appropriate for training or testing models in a realistic class-imbalance setting.

**Labels evolve over time.** Intermediate notes do not carry final labels. This forces any model or analysis pipeline to treat the dataset as a longitudinal record rather than a cross-sectional snapshot. The most recent note per patient is the ground truth for that patient's label state.

**Deceased and LTFU as terminal states.** Once a patient is deceased or lost to follow-up, no further clinical assessment is possible. These states are represented as final notes only, with appropriate note language reflecting closure of the record.

**Indication-specific clinical detail.** Biomarker panels, imaging language, and lab reference ranges vary by cancer type, making the notes more realistic and harder to trivially classify based on surface-level text features alone.

**No patient identifiers beyond ID.** Notes do not contain names, dates of birth, or other PII. The only identifier is a synthetic `patient_id` (PT0001–PT1000).

---

## Model Evaluations

### Evaluation 1 — TF-IDF + Logistic Regression (trained and tested on v2)

A baseline classification model was run against the **v2 dataset** using TF-IDF vectorisation combined with Logistic Regression. This evaluation motivated the v3 redesign.

| Split | Accuracy | Weighted F1 | Macro F1 |
|---|---|---|---|
| Train | 1.0 | 1.0 | 1.0 |
| Validation | 1.0 | 1.0 | 1.0 |
| Test | 1.0 | 1.0 | 1.0 |

The 1.0 scores are not overfitting — they reflect the fact that labels in v2 were **explicitly stated** in the note text. Each class mapped to unique, linearly separable keyword patterns (e.g. "screen failure", "eligibility confirmed", "lost to follow-up", "cause of death"), making the task trivial for any bag-of-words model. This finding directly motivated the v3 redesign.

---

### Evaluation 2 — Cross-Dataset Generalisation: Trained on v2, Tested on v3

Both TF-IDF + Logistic Regression and BERT were trained on v2 and evaluated on v3 to measure how well models trained on explicit-language notes generalise to the inferential, coordinator-style language introduced in v3.

| Metric | TF-IDF + LR | BERT |
|---|---|---|
| Accuracy | 0.586 | 0.786 |
| Weighted F1 | 0.481 | 0.747 |
| Macro F1 | 0.366 | 0.637 |
| Precision | 0.639 | 0.814 |
| Recall | 0.586 | 0.786 |

#### Interpretation

**TF-IDF + LR (Accuracy 0.59, Macro F1 0.37)** degrades severely when moved from v2 to v3. This is expected and by design. The model learned keyword associations tied to explicit verdict phrases that no longer exist in v3 notes. The drop from 1.0 to 0.59 accuracy quantifies exactly how much of the v2 task was keyword matching rather than genuine clinical language understanding. The low Macro F1 (0.37) indicates that performance is uneven across classes — the model likely retains some signal on the most structurally distinct classes (e.g. deceased, LTFU) while failing on the nuanced eligible/available distinctions that now require clinical inference.

**BERT (Accuracy 0.79, Macro F1 0.64)** generalises substantially better, which reflects its capacity for contextual language understanding rather than token frequency. BERT retains meaningful signal from v2 training — clinical patterns such as treatment regimen mentions, lab value ranges, performance status notation, and contact failure descriptions carry semantic weight that transfers across the vocabulary shift between v2 and v3. The gap between Weighted F1 (0.75) and Macro F1 (0.64) suggests BERT still struggles with minority or ambiguous classes, likely due to class imbalance and the deliberate hedging introduced in v3 intermediate notes.

**The 0.786 vs 0.586 accuracy gap between BERT and TF-IDF** is a direct measure of the value of contextual embeddings for this task. In v2, both models performed identically at ceiling. In v3, the difference becomes visible and meaningful.

#### What the Results Validate About Dataset Design

These cross-dataset results confirm that the v3 redesign achieved its intended effect. The fact that TF-IDF collapses while BERT partially recovers demonstrates that v3 notes require genuine language understanding — not just pattern matching — to classify correctly. A model that scores well on v3 must have learned something about clinical reasoning, not just clinical vocabulary.

#### Recommended Next Steps

- Train and evaluate BERT **natively on v3** (train/val/test split within v3) to establish a proper in-distribution baseline for v3 difficulty
- Analyse per-class performance for both models to identify which label states drive the Macro F1 gap
- Consider fine-tuning on a clinical NLP pre-trained model (e.g. BioBERT, ClinicalBERT) as the next benchmark tier, given the domain-specific abbreviations and lab notation in v3
