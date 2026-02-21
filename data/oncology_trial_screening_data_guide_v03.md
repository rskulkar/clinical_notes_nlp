# Oncology Trial Screening Dataset — Data Generation Guide (v3)

## Changelog

| Version | Change |
|---|---|
| v1 | Initial dataset — 1,000 patients, 3,028 notes, free-text notes with binary labels |
| v2 | Added `cancer_indication` as an explicit structured column (extracted from free-text notes). Column is positioned after `note_date` and before `free_text_note`. |
| v3 | Added final state distribution broken down by cancer indication to the data guide. |

---

## Overview

This document describes the rules, logic, and design decisions used to generate the synthetic oncology clinical trial screening dataset. The dataset is intended to simulate the kind of free-text coordinator notes maintained during patient screening for an oncology clinical trial, along with structured binary labels used for downstream analysis.

---

## Dataset Scale

| Metric | Value |
|---|---|
| Total patients | 1,000 |
| Total notes | 3,028 |
| Average notes per patient | ~3.0 |
| Note date range | January 2021 – December 2024 |
| Dataset version | v2 |

---

## Final State Distribution (Per Patient)

Distribution is measured at the level of the **most recent note** per patient, which reflects the patient's final known status.

| Label State | Count | % of Patients |
|---|---|---|
| Eligible = 1, Available = 1 | 129 | 12.9% |
| Eligible = 1, Available = 0 | 144 | 14.4% |
| Eligible = 0, Available = 1 | 182 | 18.2% |
| Eligible = 0, Available = 0 | 305 | 30.5% |
| Deceased | 95 | 9.5% |
| Lost to Follow-up | 145 | 14.5% |

The distribution is intentionally skewed to reflect realistic oncology trial screening, where the majority of screened patients do not qualify or are not available to enroll.

---

## Final State Distribution by Cancer Indication

The table below shows the final state breakdown per cancer indication, based on each patient's most recent note. Column headers match the label combinations defined above.

| Cancer Indication | N | E=1, A=1 | E=1, A=0 | E=0, A=1 | E=0, A=0 | Deceased | LTFU |
|---|---|---|---|---|---|---|---|
| Bladder Cancer | 67 | 6 | 9 | 16 | 25 | 3 | 8 |
| Breast Cancer | 72 | 12 | 8 | 14 | 20 | 11 | 7 |
| Colon Cancer | 66 | 8 | 10 | 13 | 19 | 5 | 11 |
| Colorectal Cancer | 73 | 6 | 10 | 9 | 26 | 11 | 11 |
| Endometrial Cancer | 60 | 8 | 9 | 12 | 15 | 7 | 9 |
| Gastric Cancer | 50 | 6 | 10 | 5 | 16 | 5 | 8 |
| Head and Neck Squamous Cell Carcinoma (HNSCC) | 65 | 7 | 17 | 14 | 16 | 6 | 5 |
| Hepatocellular Carcinoma | 80 | 14 | 17 | 13 | 20 | 9 | 7 |
| Melanoma | 64 | 6 | 10 | 7 | 23 | 7 | 11 |
| Non-Small Cell Lung Cancer (NSCLC) | 65 | 5 | 6 | 14 | 22 | 3 | 15 |
| Ovarian Cancer | 60 | 8 | 6 | 17 | 15 | 2 | 12 |
| Pancreatic Cancer | 72 | 9 | 13 | 9 | 22 | 6 | 13 |
| Prostate Cancer | 61 | 10 | 9 | 12 | 17 | 7 | 6 |
| Renal Cell Carcinoma | 79 | 13 | 6 | 15 | 24 | 7 | 14 |
| Small Cell Lung Cancer (SCLC) | 66 | 11 | 4 | 12 | 25 | 6 | 8 |
| **Total** | **1,000** | **129** | **144** | **182** | **305** | **95** | **145** |

**Column key:** E = Eligible, A = Available, LTFU = Lost to Follow-Up.

Notable observations from the distribution:

- **HNSCC** has the highest proportion of eligible but unavailable patients (E=1, A=0: 17/65 = 26%), suggesting many patients with this indication are on active treatment at time of screening.
- **Hepatocellular Carcinoma** has the largest patient count (n=80) and the highest absolute count of E=1, A=1 patients (14), reflecting its broad representation in the dataset.
- **NSCLC** has the highest LTFU rate (15/65 = 23%), which may reflect the aggressive disease course and challenges in long-term follow-up.
- **Ovarian Cancer** has the lowest deceased count (2/60 = 3%), while **Breast Cancer** and **Colorectal Cancer** each have the highest (11 patients each).
- **Gastric Cancer** has the smallest cohort (n=50) due to random sampling variation across 15 indications.

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

## Key Design Choices

**Realistic skew over balance.** The distribution is intentionally skewed toward ineligible and unavailable patients, mirroring real-world trial screening failure rates. This makes the dataset appropriate for training or testing models in a realistic class-imbalance setting.

**Labels evolve over time.** Intermediate notes do not carry final labels. This forces any model or analysis pipeline to treat the dataset as a longitudinal record rather than a cross-sectional snapshot. The most recent note per patient is the ground truth for that patient's label state.

**Deceased and LTFU as terminal states.** Once a patient is deceased or lost to follow-up, no further clinical assessment is possible. These states are represented as final notes only, with appropriate note language reflecting closure of the record.

**Indication-specific clinical detail.** Biomarker panels, imaging language, and lab reference ranges vary by cancer type, making the notes more realistic and harder to trivially classify based on surface-level text features alone.

**No patient identifiers beyond ID.** Notes do not contain names, dates of birth, or other PII. The only identifier is a synthetic `patient_id` (PT0001–PT1000).
