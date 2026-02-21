# Clinical Notes Classification: Oncology Trial Screening

## Project Overview

This project builds NLP models to predict patient trial eligibility status (STATUS) from free-text clinical notes in an oncology clinical trial screening database.

### Objective
Automatically classify clinical notes into one of 5 eligibility status categories:
- **AVAILABLE**: Patient meets eligibility criteria AND is available for treatment
- **ELIGIBLE**: Patient meets eligibility criteria BUT is currently unavailable
- **INELIGIBLE**: Patient does not meet eligibility criteria
- **CENSORED**: Patient is lost to follow-up
- **DECEASED**: Patient has passed away

### Dataset
- **Source**: `oncology_trial_screening_v02.csv`
- **Patients**: 1,000 unique patients
- **Notes**: 3,028 total notes (multiple notes per patient)
- **Data Used**: Most recent note per patient only
- **Split**: 70% train, 15% validation, 15% test (stratified by STATUS)
- **Class Distribution**: Imbalanced (INELIGIBLE: 30.5%, AVAILABLE: 12.9%, CENSORED: 14.5%, ELIGIBLE: 14.4%, DECEASED: 9.5%)

### Label Creation Rules
STATUS labels are derived from four binary columns with the following priority:
1. If `deceased = 1` → `DECEASED`
2. Elif `lost_to_follow_up = 1` → `CENSORED`
3. Elif `available = 1 AND eligible = 1` → `AVAILABLE`
4. Elif `available = 0 AND eligible = 1` → `ELIGIBLE`
5. Else → `INELIGIBLE`

---

## Models Implemented

### Approach #1: TF-IDF + Logistic Regression
**Notebook**: `02_tfidf_logistic_regression.ipynb`

A classical NLP approach using:
- **Text Representation**: TF-IDF vectorization (5,000 features, max_df=0.95, min_df=2)
- **Classification**: Logistic Regression (multinomial, 1000 iterations)
- **Preprocessing**:
  - Lowercase
  - Tokenization
  - Numerical value removal (keeps clinical abbreviations like "ECOG PS", "CT")
  - English stopword removal
  - Unigrams and bigrams (ngram_range=(1,2))

**Advantages**:
- Fast training and inference
- Interpretable (feature importance visible)
- Low memory requirements
- Works well with smaller datasets

### Approach #2: Fine-tuned BERT
**Notebook**: `03_bert_finetuning.ipynb`

A deep learning approach using:
- **Base Model**: `bert-base-uncased` (HuggingFace)
- **Architecture**: BERT + Classification Head
- **Training**:
  - Tokenization: BERT tokenizer (max_length=512)
  - Optimizer: AdamW (lr=2e-5)
  - Learning Rate Scheduler: Linear warmup (10% warmup steps)
  - Batch Size: 16
  - Epochs: 5 (with early stopping, patience=2)
  - Loss: CrossEntropyLoss

**Advantages**:
- Captures semantic context and linguistic patterns
- Transfer learning from pre-trained weights
- Better handling of complex language structures
- State-of-the-art performance potential

---

## Project Structure

```
code/
├── 01_data_preparation.ipynb          # Data loading, filtering, label creation, splitting
├── 02_tfidf_logistic_regression.ipynb # TF-IDF + Logistic Regression model
├── 03_bert_finetuning.ipynb           # BERT fine-tuning
├── 04_model_comparison.ipynb          # Model comparison and recommendations
├── README.md                          # This file
├── requirements.txt                   # Python dependencies
└── colab_setup.sh                     # Optional setup script for Google Colab

Output files (generated during notebook execution):
├── processed_data.csv                 # Full dataset with STATUS labels and splits
├── train_data.csv                     # Training set
├── validation_data.csv                # Validation set
├── test_data.csv                      # Test set
├── class_mapping.json                 # Class-to-index mapping
├── tfidf_model.pkl                    # Trained TF-IDF + LR model
├── tfidf_vectorizer.pkl               # TF-IDF vectorizer
├── tfidf_metrics.json                 # TF-IDF metrics
├── bert_model_finetuned/              # Fine-tuned BERT model directory
├── bert_metrics.json                  # BERT metrics
├── Various PNG visualizations         # Confusion matrices, ROC curves, etc.
└── SUMMARY_REPORT.txt                 # Final summary report
```

---

## Installation and Setup

### Local Installation

1. **Clone the repository** (or download the code directory)
   ```bash
   git clone <repo_url>
   cd clinical_notes_classification/code
   ```

2. **Create a Python virtual environment** (recommended)
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Ensure data file is in place**
   - The file `../data/oncology_trial_screening_v02.csv` should exist
   - Update the `data_path` variable in notebooks if needed

### Google Colab Setup

#### Option A: Using the provided setup script

1. **Upload files to Google Drive**
   - Create a folder structure in Google Drive: `My Drive/clinical_notes_classification/code`
   - Upload all notebooks and `requirements.txt`
   - Upload the CSV file to `My Drive/clinical_notes_classification/data/`

2. **In a Colab cell, run the setup script**
   ```bash
   !curl -O https://path/to/colab_setup.sh
   !bash colab_setup.sh
   ```

#### Option B: Manual setup in Colab

1. **Open a notebook in Google Colab**

2. **Mount Google Drive** (first cell of notebook)
   ```python
   from google.colab import drive
   drive.mount('/content/drive')
   ```

3. **Install dependencies** (first cell after mounting)
   ```bash
   !pip install -r "/content/drive/My Drive/clinical_notes_classification/code/requirements.txt"
   ```

4. **Change directory and update data path**
   ```python
   import os
   os.chdir('/content/drive/My Drive/clinical_notes_classification/code')

   # Update data_path in notebook:
   data_path = '/content/drive/My Drive/clinical_notes_classification/data/oncology_trial_screening_v02.csv'
   ```

5. **Run notebook cells sequentially**

---

## Running the Notebooks

### Recommended Execution Order

#### **Step 1: Data Preparation** (10 minutes)
```python
# Run: 01_data_preparation.ipynb
```
**Outputs**:
- `processed_data.csv` - Full dataset with STATUS labels
- `train_data.csv`, `validation_data.csv`, `test_data.csv` - Split datasets
- `class_mapping.json` - Class-to-index mapping
- Visualizations: `class_distribution.png`, `split_distribution.png`

#### **Step 2A: Train TF-IDF + Logistic Regression** (5 minutes)
```python
# Run: 02_tfidf_logistic_regression.ipynb
```
**Outputs**:
- `tfidf_model.pkl` - Trained model
- `tfidf_vectorizer.pkl` - TF-IDF vectorizer
- `tfidf_metrics.json` - Performance metrics
- Visualizations: Confusion matrices, ROC curves, feature importance

#### **Step 2B: Fine-tune BERT** (30-60 minutes on Colab GPU)
```python
# Run: 03_bert_finetuning.ipynb
```
**Outputs**:
- `best_bert_model.pt` - Best model checkpoint
- `bert_model_finetuned/` - Full model directory
- `bert_metrics.json` - Performance metrics
- Visualizations: Confusion matrices, ROC curves, training curves

#### **Step 3: Compare Models** (5 minutes)
```python
# Run: 04_model_comparison.ipynb
```
**Outputs**:
- Side-by-side performance comparison
- Recommendations for deployment
- `SUMMARY_REPORT.txt` - Final report
- Visualizations: Comparison charts

---

## Expected Results

### Performance Metrics (on Test Set)

**TF-IDF + Logistic Regression**:
- Weighted F1: ~0.65-0.75
- Accuracy: ~0.65-0.75
- Fast training and inference

**Fine-tuned BERT**:
- Weighted F1: ~0.70-0.80
- Accuracy: ~0.70-0.80
- Better performance, slower inference

> Note: Exact values depend on random seed and computational environment

### Key Observations

1. **Class Imbalance Impact**: INELIGIBLE class dominates, reducing overall F1 scores
2. **BERT Advantage**: Better at capturing contextual relationships in clinical text
3. **TF-IDF Advantage**: More interpretable, faster, suitable for production environments with limited resources
4. **Minority Classes**: AVAILABLE and DECEASED classes have lower per-class F1 due to fewer samples

---

## Evaluation Metrics Explained

### Primary Metric: Weighted F1-Score
- Accounts for class imbalance
- Weights each class by its support (number of samples)
- **Best for imbalanced classification**
- Range: 0.0 (worst) to 1.0 (best)

### Secondary Metrics
- **Macro F1**: Unweighted average, gives equal importance to all classes
- **Accuracy**: Overall correctness (less meaningful with imbalanced data)
- **Precision/Recall**: Per-class performance
- **Confusion Matrix**: Shows misclassification patterns
- **ROC-AUC**: Probability that model ranks a random positive example higher than a random negative example

---

## Feature Importance (TF-IDF Model)

Top features for each class reflect clinical terminology:
- **AVAILABLE**: "stable", "eligible", "available", "interested", "start"
- **ELIGIBLE**: "eligible", "criteria", "meet", "stable", "disease"
- **INELIGIBLE**: "ineligible", "exclude", "failure", "criterion", "inadequate"
- **DECEASED**: "deceased", "death", "died", "failure"
- **CENSORED**: "lost", "follow-up", "unable", "reach", "unreachable"

---

## Recommendations for Improvement

### Short-term (Next Iteration)
1. **Class Weighting**: Apply higher loss weights to minority classes (DECEASED, AVAILABLE)
2. **Hyperparameter Tuning**: Grid search over learning rates, batch sizes
3. **Feature Engineering**: Extract structured features (disease status, treatment, lab values)

### Medium-term (Future Work)
1. **Clinical BERT Variants**: Try BioBERT, ClinicalBERT, SciBERT
2. **Ensemble Methods**: Combine TF-IDF and BERT predictions
3. **Data Collection**: Gather more samples, especially for minority classes
4. **Entity Extraction**: Extract clinical entities (medications, procedures, symptoms)

### Long-term (Advanced)
1. **Multi-task Learning**: Jointly predict STATUS and other relevant outcomes
2. **Active Learning**: Identify uncertain samples for manual labeling
3. **Explainability**: LIME or SHAP to explain individual predictions
4. **Domain Adaptation**: Fine-tune on your specific trial's note patterns

---

## Deployment Guide

### Using TF-IDF + Logistic Regression
```python
import pickle
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

# Load model and vectorizer
with open('tfidf_model.pkl', 'rb') as f:
    model = pickle.load(f)
with open('tfidf_vectorizer.pkl', 'rb') as f:
    vectorizer = pickle.load(f)

# Preprocess and predict
text = "Patient with cancer..."
text_vectorized = vectorizer.transform([text])
prediction = model.predict(text_vectorized)[0]
probability = model.predict_proba(text_vectorized)[0]
```

### Using Fine-tuned BERT
```python
from transformers import BertTokenizer, BertForSequenceClassification
import torch
import json

# Load model
tokenizer = BertTokenizer.from_pretrained('bert_model_finetuned')
model = BertForSequenceClassification.from_pretrained('bert_model_finetuned')

# Load class mapping
with open('class_mapping.json') as f:
    class_mapping = json.load(f)
reverse_mapping = {v: k for k, v in class_mapping.items()}

# Predict
text = "Patient with cancer..."
inputs = tokenizer(text, return_tensors='pt', max_length=512, truncation=True, padding=True)
with torch.no_grad():
    outputs = model(**inputs)
    logits = outputs.logits
    probabilities = torch.softmax(logits, dim=1)[0]
    prediction_idx = torch.argmax(logits, dim=1)[0].item()
    prediction = reverse_mapping[prediction_idx]
```

---

## Troubleshooting

### Issue: CUDA Out of Memory in Colab (BERT Training)
**Solution**:
- Reduce batch size from 16 to 8
- Set `max_length=256` instead of 512
- Use `torch.cuda.empty_cache()` between epochs

### Issue: Slow Training on CPU
**Solution**:
- Use Google Colab with GPU acceleration (Runtime → Change runtime type → GPU)
- For TF-IDF, CPU is acceptable
- For BERT, GPU highly recommended

### Issue: Data File Not Found
**Solution**:
- Verify file path in notebook
- For Colab: ensure file is in Google Drive at expected location
- Use absolute paths instead of relative paths

### Issue: ImportError for transformers/torch
**Solution**:
```bash
pip install --upgrade torch transformers
```

---

## References and Resources

- **Data Guide**: `../data/oncology_trial_screening_data_guide_v03.md`
- **BERT Documentation**: https://huggingface.co/bert-base-uncased
- **Scikit-learn**: https://scikit-learn.org/
- **HuggingFace Transformers**: https://huggingface.co/docs/transformers

---

## Citation

If you use this project, please cite:
```
Clinical Notes Classification for Oncology Trial Screening
Author: [Your Name/Organization]
Year: 2026
Dataset: Synthetic oncology trial screening database (1,000 patients)
```

---

## License

[Specify your license, e.g., MIT, Apache 2.0, etc.]

---

## Support and Questions

For questions or issues:
1. Check the troubleshooting section above
2. Review notebook comments and markdown cells
3. Consult the data guide for context
4. Refer to HuggingFace and scikit-learn documentation

---

**Last Updated**: February 2026
