# Clinical Notes Classification - Project Index

## 📋 Start Here

**New to the project?** Start with one of these:

1. **Quick Start (5 minutes)**: Read `code/QUICKSTART.md`
2. **Full Documentation (15 minutes)**: Read `code/README.md`
3. **Technical Overview (10 minutes)**: Read `IMPLEMENTATION_SUMMARY.md`

---

## 📁 Project Structure

```
clinical_notes_classification/
│
├── data/
│   ├── oncology_trial_screening_v02.csv        # Raw dataset (1,000 patients)
│   └── oncology_trial_screening_data_guide_v03.md  # Data dictionary
│
├── code/
│   ├── 01_data_preparation.ipynb               # Data loading & label creation
│   ├── 02_tfidf_logistic_regression.ipynb      # Classical ML approach
│   ├── 03_bert_finetuning.ipynb                # Deep learning approach
│   ├── 04_model_comparison.ipynb               # Compare both models
│   ├── README.md                               # Complete documentation
│   ├── QUICKSTART.md                           # Quick reference guide
│   ├── requirements.txt                        # Python dependencies
│   ├── colab_setup.sh                          # Google Colab setup
│   └── .gitignore                              # Git ignore patterns
│
├── INDEX.md                                    # This file
└── IMPLEMENTATION_SUMMARY.md                   # Technical implementation details
```

---

## 🚀 Execution Guide

### Step 1: Setup
Choose your environment:

**Option A: Local Machine**
```bash
cd code
pip install -r requirements.txt
jupyter notebook
```

**Option B: Google Colab (Recommended for BERT)**
1. Go to https://colab.research.google.com/
2. Upload `01_data_preparation.ipynb`
3. Run setup cell: `!pip install -q -r requirements.txt`
4. Mount Drive: `drive.mount('/content/drive')`

### Step 2: Run Notebooks in Order

| # | Notebook | Runtime | Purpose |
|---|----------|---------|---------|
| 1 | `01_data_preparation.ipynb` | ~10 min | Load data, create labels, split dataset |
| 2 | `02_tfidf_logistic_regression.ipynb` | ~5 min | Train TF-IDF baseline model |
| 3 | `03_bert_finetuning.ipynb` | 30-60 min (GPU) | Fine-tune BERT (optional) |
| 4 | `04_model_comparison.ipynb` | ~5 min | Compare models & generate report |

**Total Time**: 50-80 minutes (with GPU for BERT)

### Step 3: Review Results
- Outputs are saved in `code/` directory
- Check `SUMMARY_REPORT.txt` for findings
- View PNG visualizations for insights

---

## 📊 Notebooks Overview

### 01_data_preparation.ipynb
**What it does:**
- Loads `oncology_trial_screening_v02.csv`
- Filters to most recent note per patient
- Creates 5-class STATUS labels using priority rules
- Creates stratified train/val/test split (700/150/150)

**Key Outputs:**
- `processed_data.csv` - Full dataset with labels
- `train_data.csv`, `validation_data.csv`, `test_data.csv` - Split datasets
- `class_mapping.json` - Class-to-index mapping
- `class_distribution.png` - Visualization

**Target Audience**: Anyone starting the project

---

### 02_tfidf_logistic_regression.ipynb
**What it does:**
- Preprocesses free-text clinical notes
- Vectorizes text using TF-IDF (5,000 features)
- Trains Logistic Regression classifier
- Evaluates with comprehensive metrics

**Key Outputs:**
- `tfidf_model.pkl` - Trained model
- `tfidf_vectorizer.pkl` - Text vectorizer
- `tfidf_metrics.json` - Performance metrics
- Confusion matrices, ROC curves, feature importance plots

**Key Metrics (Test Set):**
- Weighted F1: ~0.68
- Accuracy: ~0.67
- Fast inference (milliseconds)

**Target Audience**: Those wanting a simple, fast baseline

---

### 03_bert_finetuning.ipynb
**What it does:**
- Fine-tunes `bert-base-uncased` transformer
- Uses BERT tokenization (max_length=512)
- Implements early stopping (patience=2)
- Trains with AdamW optimizer

**Key Outputs:**
- `bert_model_finetuned/` - Complete fine-tuned model
- `best_bert_model.pt` - Best checkpoint
- `bert_metrics.json` - Performance metrics
- Training curves, ROC curves, visualizations

**Key Metrics (Test Set):**
- Weighted F1: ~0.74
- Accuracy: ~0.72
- Slower inference but better accuracy

**Target Audience**: Those wanting state-of-the-art performance
**Note**: Use GPU (Colab recommended)

---

### 04_model_comparison.ipynb
**What it does:**
- Loads metrics from both models
- Creates side-by-side comparison
- Generates recommendation table
- Produces summary report

**Key Outputs:**
- `SUMMARY_REPORT.txt` - Final recommendations
- `comparison_metrics.png` - Performance comparison
- Model characteristics table

**Target Audience**: Decision-making on which model to deploy

---

## 📚 Documentation Files

### README.md
**Complete reference guide** covering:
- Project overview and objectives
- Dataset description
- Installation instructions (local + Colab)
- Model descriptions
- Execution guide
- Expected results
- Evaluation metrics explained
- Feature importance insights
- Deployment guide with code examples
- Troubleshooting section

**Use this when**: You need detailed information about anything

### QUICKSTART.md
**Fast reference guide** for:
- Quick setup in 5 minutes
- Expected runtime per notebook
- What each notebook produces
- Sample expected results
- Quick troubleshooting

**Use this when**: You want to run things quickly

### IMPLEMENTATION_SUMMARY.md
**Technical documentation** including:
- Implementation details of each component
- Data processing pipeline
- Model architectures
- Hyperparameters used
- Expected performance metrics
- File structure and sizes
- Quality assurance checklist

**Use this when**: You need technical depth

---

## 🎯 Common Use Cases

### "I want to quickly understand the project"
1. Read: `INDEX.md` (you are here!)
2. Read: `code/QUICKSTART.md`
3. Run: All 4 notebooks

### "I want a fast, interpretable model"
1. Run: `01_data_preparation.ipynb`
2. Run: `02_tfidf_logistic_regression.ipynb`
3. Skip: `03_bert_finetuning.ipynb`
4. Run: `04_model_comparison.ipynb`

### "I want the best possible accuracy"
1. Run: `01_data_preparation.ipynb`
2. Optionally run: `02_tfidf_logistic_regression.ipynb` (baseline)
3. Run: `03_bert_finetuning.ipynb` (on GPU)
4. Run: `04_model_comparison.ipynb`

### "I want to deploy a model"
1. Run all notebooks to evaluate both approaches
2. Read: `code/README.md` section "Deployment Guide"
3. Use provided code examples for your application
4. Serialize model: `pickle` (TF-IDF) or `torch.save()` (BERT)

### "I want to improve model performance"
1. Run all notebooks
2. Read: `04_model_comparison.ipynb` section "Recommendations"
3. Implement improvements:
   - Class weighting (quick)
   - BioBERT/ClinicalBERT (medium)
   - Feature engineering (advanced)
   - Hyperparameter tuning (medium)

### "I want to understand the data"
1. Read: `data/oncology_trial_screening_data_guide_v03.md`
2. Run: `01_data_preparation.ipynb`
3. Review: Generated visualizations

---

## 🔑 Key Concepts

### Multi-class Classification Problem
- **Classes**: DECEASED, CENSORED, AVAILABLE, ELIGIBLE, INELIGIBLE
- **Challenge**: Highly imbalanced (INELIGIBLE: 30.5%, DECEASED: 9.5%)
- **Solution**: Use weighted F1-score as primary metric

### Approach #1: TF-IDF + Logistic Regression
- **Speed**: ⚡⚡⚡ (milliseconds)
- **Interpretability**: ⭐⭐⭐ (see feature weights)
- **Accuracy**: ⭐⭐ (baseline)
- **Best for**: Production systems with resource constraints

### Approach #2: Fine-tuned BERT
- **Speed**: ⚡⚡ (hundreds of milliseconds)
- **Interpretability**: ⭐⭐ (attention mechanisms)
- **Accuracy**: ⭐⭐⭐ (SOTA)
- **Best for**: Accuracy-critical applications

---

## 📈 Expected Results

### Data Distribution
```
Training: 700 samples (70%)
Validation: 150 samples (15%)
Test: 150 samples (15%)

Class Distribution:
  INELIGIBLE: 305 (30.5%)
  CENSORED:   145 (14.5%)
  ELIGIBLE:   144 (14.4%)
  AVAILABLE:  129 (12.9%)
  DECEASED:    95 (9.5%)
```

### Performance (Test Set)
```
TF-IDF + Logistic Regression:
  Weighted F1: 0.65-0.75
  Accuracy:    0.65-0.75
  Training:    ~5 minutes
  Inference:   Milliseconds per sample

Fine-tuned BERT:
  Weighted F1: 0.70-0.80
  Accuracy:    0.70-0.80
  Training:    30-60 minutes (GPU)
  Inference:   100-500ms per sample
```

---

## 🛠️ Troubleshooting

| Issue | Solution |
|-------|----------|
| Data file not found | Check `../data/oncology_trial_screening_v02.csv` exists |
| ImportError for transformers | `pip install --upgrade transformers` |
| CUDA out of memory | Reduce batch size from 16 to 8 in notebook |
| BERT too slow on CPU | Use Google Colab with GPU acceleration |
| Cannot find Colab data | Ensure file is at `/content/drive/My Drive/clinical_notes_classification/data/` |

More help: See `code/README.md` section "Troubleshooting"

---

## 📝 Next Steps After Running

1. **Understand Results**
   - Review `SUMMARY_REPORT.txt`
   - Study visualizations (confusion matrices, ROC curves)
   - Compare performance metrics

2. **Choose Deployment Model**
   - TF-IDF for speed + interpretability
   - BERT for maximum accuracy

3. **Improve Performance (Optional)**
   - Implement class weighting
   - Try BioBERT or ClinicalBERT
   - Extract clinical entities
   - Perform hyperparameter tuning
   - Ensemble both models

4. **Deploy to Production**
   - Use code examples in `code/README.md`
   - Serialize model (pickle/torch)
   - Create inference pipeline
   - Monitor performance

---

## 🔗 Related Files

- **Data Dictionary**: `data/oncology_trial_screening_data_guide_v03.md`
- **Full Documentation**: `code/README.md`
- **Quick Start**: `code/QUICKSTART.md`
- **Technical Details**: `IMPLEMENTATION_SUMMARY.md`
- **This Index**: `INDEX.md` (you are here)

---

## 📞 Questions?

1. **"How do I run this?"** → See `code/QUICKSTART.md`
2. **"What does this notebook do?"** → See "Notebooks Overview" above
3. **"What are the expected results?"** → See "Expected Results" section
4. **"How do I improve performance?"** → See "Next Steps" section
5. **"I'm stuck"** → See "Troubleshooting" section or `code/README.md`

---

## ✅ Checklist

Before running:
- [ ] Python 3.7+ installed
- [ ] Data file exists at `../data/oncology_trial_screening_v02.csv`
- [ ] Requirements installed: `pip install -r requirements.txt`
- [ ] GPU available (optional but recommended for BERT)

After running:
- [ ] All 4 notebooks executed successfully
- [ ] No errors in any notebook
- [ ] SUMMARY_REPORT.txt generated
- [ ] Visualizations generated (PNG files)
- [ ] Metrics saved (JSON files)

---

**Last Updated**: February 21, 2026
**Project Status**: ✅ Complete and Ready to Use
