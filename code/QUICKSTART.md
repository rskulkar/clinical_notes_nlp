# Quick Start Guide

## Running on Your Local Machine (5 minutes setup)

### 1. Install Dependencies
```bash
cd clinical_notes_classification/code
pip install -r requirements.txt
```

### 2. Run Notebooks in Order
```bash
# Terminal 1: Start Jupyter
jupyter notebook

# In browser: Open notebooks one by one
01_data_preparation.ipynb          # ~10 min
02_tfidf_logistic_regression.ipynb # ~5 min
03_bert_finetuning.ipynb           # Skip if no GPU (or ~30-60 min with GPU)
04_model_comparison.ipynb          # ~5 min
```

---

## Running on Google Colab (Recommended for BERT)

### Quick Setup (2 steps)

**Step 1: Copy to Colab** (in Colab cell)
```python
# Mount Google Drive
from google.colab import drive
drive.mount('/content/drive')

# Install dependencies
!pip install -q pandas numpy matplotlib seaborn scikit-learn torch transformers
```

**Step 2: Navigate and Run**
```python
import os
os.chdir('/content/drive/My\ Drive/clinical_notes_classification/code')

# Verify data file exists
!ls ../data/
```

Then run each notebook cell-by-cell.

---

## Key Files Generated

| Notebook | Key Outputs |
|----------|------------|
| **01 - Data Prep** | `processed_data.csv`, `train_data.csv`, `test_data.csv`, `class_mapping.json` |
| **02 - TF-IDF** | `tfidf_model.pkl`, `tfidf_metrics.json`, confusion matrices, ROC curves |
| **03 - BERT** | `bert_model_finetuned/`, `bert_metrics.json`, training curves |
| **04 - Compare** | `SUMMARY_REPORT.txt`, comparison visualizations |

---

## Expected Runtime

| Notebook | Local CPU | Colab GPU |
|----------|-----------|-----------|
| 01 - Data Prep | ~10 min | ~5 min |
| 02 - TF-IDF | ~5 min | ~3 min |
| 03 - BERT | ⏭️ Skip or ~2-3 hours | ~30-60 min |
| 04 - Compare | ~5 min | ~3 min |

**⏭️ = Skip BERT on CPU (too slow), use Colab GPU instead**

---

## What Each Notebook Does

### 📊 `01_data_preparation.ipynb`
- Loads raw CSV data
- Filters to latest note per patient
- Creates STATUS labels using priority rules
- Creates stratified train/val/test split (70/15/15)
- **Output**: `processed_data.csv`

### 🎯 `02_tfidf_logistic_regression.ipynb`
- Vectorizes text using TF-IDF
- Trains Logistic Regression classifier
- Evaluates: Accuracy, Weighted F1, Macro F1, Confusion Matrix, ROC-AUC
- Shows top features per class
- **Output**: Trained model + visualizations

### 🤖 `03_bert_finetuning.ipynb`
- Fine-tunes `bert-base-uncased` from HuggingFace
- Early stopping (patience=2)
- Same evaluation metrics as TF-IDF
- Shows training curves
- **Output**: Fine-tuned model + visualizations

### 📈 `04_model_comparison.ipynb`
- Compares performance of both models
- Side-by-side visualizations
- Recommendations for deployment
- Summary report
- **Output**: `SUMMARY_REPORT.txt`

---

## Sample Results (Expected)

**TF-IDF + Logistic Regression** (Test Set):
```
Weighted F1: 0.68
Accuracy:    0.67
Fast inference, interpretable
```

**Fine-tuned BERT** (Test Set):
```
Weighted F1: 0.74
Accuracy:    0.72
Better performance, slower but still reasonable
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| **Data file not found** | Check `../data/oncology_trial_screening_v02.csv` exists |
| **BERT too slow on CPU** | Use Google Colab with GPU |
| **CUDA out of memory** | Reduce batch size from 16 to 8 in `03_bert_finetuning.ipynb` |
| **Import errors** | Run `pip install --upgrade -r requirements.txt` |
| **Colab: File not found** | Ensure file is at `/content/drive/My Drive/clinical_notes_classification/data/` |

---

## What to Try Next (if running locally)

1. ✅ Run all 4 notebooks sequentially
2. ✅ Review the visualizations (confusion matrices, ROC curves, feature importance)
3. ✅ Read `SUMMARY_REPORT.txt` for recommendations
4. 🔄 Try class weighting (modify notebook 02 or 03)
5. 🔄 Test with clinical BERT variants (BioBERT, ClinicalBERT)

---

## Need Help?

1. **Full documentation**: See `README.md`
2. **Data dictionary**: See `../data/oncology_trial_screening_data_guide_v03.md`
3. **Notebook comments**: Each cell has markdown explanations

---

**Estimated total runtime**: 30-90 minutes (depending on hardware)

Good luck! 🚀
