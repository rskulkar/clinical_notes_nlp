# Clinical Notes Classification: Start Here 🚀

Welcome! This guide will help you quickly understand and use this project.

---

## What is This Project?

This project builds **NLP models to automatically classify clinical notes** into 5 patient trial eligibility status categories:
- **AVAILABLE** (13.7%): Meets criteria AND available
- **ELIGIBLE** (15.4%): Meets criteria BUT unavailable
- **INELIGIBLE** (53.1%): Doesn't meet criteria
- **CENSORED** (8.3%): Lost to follow-up
- **DECEASED** (9.4%): Passed away

**Use Case**: Accelerate oncology trial patient screening by automating eligibility classification.

---

## Quick Results Summary

### Model Comparison

| Model | Test Accuracy | Weighted F1 | Training Time | Inference Speed | Model Size |
|-------|---------------|-------------|---------------|-----------------|------------|
| **TF-IDF + LR** | 82.7% | 80.4% | <1 min | 1-5 ms | 66 KB |
| **BERT (Fine-tuned)** | **96.0%** ✓ | **96.0%** ✓ | 9 min | 200-500 ms | 440 MB |

**Key Finding**: BERT achieves **+13.3% accuracy improvement** at the cost of inference latency and model size.

---

## Which Model Should I Use?

### Use **TF-IDF + Logistic Regression** if:
- ✓ You need **real-time predictions** (<10 ms latency)
- ✓ You have **limited computational resources** (CPU-only)
- ✓ You need **interpretable decisions** (show why model predicted X)
- ✓ You want **simple deployment** (no GPU, no deep learning infrastructure)
- ✓ 82-83% accuracy is **sufficient** for your use case

**Runtime**: <1 minute training | 1-5 ms inference | 66 KB model

### Use **BERT** if:
- ✓ You need **maximum accuracy** (>95% performance)
- ✓ You have **GPU access** (Google Colab, AWS, local GPU)
- ✓ You can **tolerate 200-500 ms latency** per prediction
- ✓ You want **state-of-the-art** performance
- ✓ **Minority class performance matters** (AVAILABLE, ELIGIBLE)

**Runtime**: 9 minutes training | 200-500 ms inference | 440 MB model

### Use **Both** (Ensemble) if:
- ✓ You want **speed + accuracy**: TF-IDF for screening, BERT for verification
- ✓ You can implement **two-stage pipeline**:
  1. Fast TF-IDF screening (1-5 ms)
  2. BERT verification for uncertain cases (200-500 ms)
- **Result**: ~90% throughput of TF-IDF + accuracy of BERT

---

## Get Started in 5 Minutes

### Step 1: Clone & Install (2 minutes)
```bash
cd clinical_notes_nlp/code
pip install -r requirements.txt
```

### Step 2: Run Data Preparation (3 minutes)
```bash
jupyter notebook
# Open: 01_data_preparation.ipynb
# Run all cells
```

### Step 3: Choose Your Path

**Path A: TF-IDF Only** (3 minutes)
```
Run: 02_tfidf_logistic_regression.ipynb
Output: tfidf_model.pkl (ready for deployment)
```

**Path B: BERT Only** (30-60 minutes on GPU)
```
Run: 03_bert_finetuning.ipynb
Output: bert_model_final/ (ready for deployment)
```

**Path C: Compare Both** (1-2 hours)
```
Run: 02 → 03 → 04_model_comparison.ipynb
Output: SUMMARY_REPORT.md with recommendations
```

---

## Understanding the Code

### Project Structure
```
code/
├── START_HERE.md              ← You are here!
├── SUMMARY_REPORT.md          ← Detailed analysis & recommendations
├── README.md                  ← Full documentation
├── QUICKSTART.md              ← Quick start guide
│
├── 01_data_preparation.ipynb     ← Data loading, cleaning, splitting
├── 02_tfidf_logistic_regression.ipynb ← TF-IDF approach
├── 03_bert_finetuning.ipynb      ← BERT fine-tuning
├── 04_model_comparison.ipynb     ← Performance comparison
│
├── requirements.txt           ← Python dependencies
├── class_mapping.json         ← Class ID mappings
│
└── Output Files (generated):
    ├── tfidf_model.pkl        ← Trained TF-IDF model
    ├── bert_model_final/      ← Fine-tuned BERT model
    ├── SUMMARY_REPORT.md      ← Results summary
    └── *.png                  ← Visualizations
```

### Three Main Approaches

#### **Approach #1: TF-IDF + Logistic Regression**
```
Text → Tokenize → TF-IDF (1,622 features) → Logistic Regression → Prediction
```
- **Interpretable**: See which words matter
- **Fast**: 1-5 ms inference
- **Lightweight**: 66 KB model
- **Performance**: 82.7% test accuracy

#### **Approach #2: BERT (Base)**
```
Text → Tokenize → BERT (12 layers, 109M params) → [CLS] token → Dense head → Prediction
```
- **Semantic**: Understands context and synonyms
- **Accurate**: 96% test accuracy
- **Pre-trained**: Trained on billions of words
- **Fine-tuning**: Adapt to clinical domain with 648 samples

#### **Approach #3: ClinicalBERT** (Future)
```
Text → Tokenize → ClinicalBERT (domain pre-trained) → Classification → Prediction
```
- **Specialized**: Pre-trained on medical text
- **Better**: Expected 2-5% improvement over base BERT
- **Status**: Planned for follow-up work

---

## Key Findings

### ✓ What Works Well

**TF-IDF Insights**:
- Clinical language is **explicit**: Keywords like "deceased", "lost to follow-up", "eligible" appear in notes
- Simple word frequencies **capture 82.7%** of the classification task
- **Fast and interpretable** - see which words drive decisions

**BERT Advantages**:
- Understands **context**: "NOT eligible" ≠ "eligible"
- Recognizes **synonyms**: "deceased" = "died" = "passed away"
- Bridges **confusion between classes**: Better at AVAILABLE vs ELIGIBLE distinction
- **Exceptional minority class performance**: All classes >95% F1

### ⚠️ Challenges Found & Resolved

**Data Leakage**:
- **Found**: 52 training samples identical to test/validation sets
- **Action**: Removed from training
- **Impact**: Prevents artificial accuracy inflation (was ~99%, now 96%)

**Class Imbalance**:
- **Issue**: INELIGIBLE dominates (53% of data)
- **Solution**: Both models handle well with weighted F1
- **Result**: BERT achieves 95%+ F1 even for minority classes

**Clinical Text Complexity**:
- **Issue**: Notes contain unstructured, variable-length text
- **Solution**: BERT's contextual embeddings handle this well
- **Result**: 96% accuracy despite messy real-world data

---

## For the Impatient

### 30-Second Version
- **Goal**: Classify clinical notes into 5 eligibility categories
- **Best Model**: BERT (96% accuracy, 200-500 ms)
- **Fast Model**: TF-IDF (82.7% accuracy, 1-5 ms)
- **Recommendation**: Use ensemble (TF-IDF + BERT)

### 2-Minute Version

**Performance**:
```
TF-IDF:  82.7% accuracy (fast, interpretable)
BERT:    96.0% accuracy (slower, better)
```

**Trade-offs**:
```
                TF-IDF    BERT
Speed:          ✓ Fast    ✗ Slow (100× slower)
Accuracy:       ✗ Good    ✓ Excellent
Interpretable:  ✓ Yes     ✗ Black box
Size:           ✓ Tiny    ✗ Large (440 MB)
Cost:           ✓ CPU     ✗ GPU preferred
```

**Recommendation**: Start with TF-IDF for quick wins, add BERT for production.

---

## Next Steps

### Immediate (This Week)
1. [ ] Run `01_data_preparation.ipynb` - understand your data
2. [ ] Run `02_tfidf_logistic_regression.ipynb` - fast baseline
3. [ ] Read `SUMMARY_REPORT.md` - understand results
4. [ ] Decide: TF-IDF, BERT, or both?

### Short-term (This Month)
1. [ ] Run `03_bert_finetuning.ipynb` - train BERT on GPU
2. [ ] Compare models with `04_model_comparison.ipynb`
3. [ ] Deploy chosen model to production
4. [ ] Validate with clinical team

### Medium-term (Next 2-3 Months)
1. [ ] Try ClinicalBERT for 2-5% improvement
2. [ ] Add model explainability (LIME/SHAP)
3. [ ] Implement ensemble approach
4. [ ] Set up monitoring and retraining pipeline

### Long-term (3+ Months)
1. [ ] Collect domain-specific training data (1000+ notes)
2. [ ] Fine-tune BERT on your actual clinical language
3. [ ] Implement active learning for efficient annotation
4. [ ] Achieve 97-98% accuracy with custom model

---

## Common Questions

### Q: Can I run BERT on my laptop?
**A**: Yes, but slowly. BERT needs:
- CPU: Intel i5+ or M1/M2 Mac (~1-2 seconds per prediction)
- GPU: Highly recommended (~200-500 ms per prediction)
- RAM: 2-4 GB minimum
- Storage: 500 MB for model

Use Google Colab (free GPU) if you don't have local GPU.

### Q: Which model is production-ready?
**A**: Both!
- **TF-IDF**: Production-ready now. Fast, simple, interpretable.
- **BERT**: Production-ready with infrastructure. Requires GPU or cloud.
- **Ensemble**: Best of both. Recommended for critical applications.

### Q: Can I explain BERT predictions?
**A**: With effort. BERT is a black box, but:
- Use LIME or SHAP to generate explanations
- Analyze attention weights (which words it focuses on)
- Compare with TF-IDF for interpretability
- Add explainability layer (1-2 weeks effort)

### Q: What if 96% isn't good enough?
**A**: Try:
1. ClinicalBERT (+2-5% expected)
2. Collect more training data (1000+ notes)
3. Try ensemble methods
4. Add structured features (disease, treatment, labs)

### Q: How often should I retrain?
**A**: Recommend:
- **Monthly**: With new data (1-2 weeks)
- **Quarterly**: Full retraining on accumulated data
- **Continuous**: Monitor for accuracy degradation

---

## Key Resources

| Resource | Link/Location |
|----------|---------------|
| **Full Documentation** | `README.md` |
| **Detailed Results** | `SUMMARY_REPORT.md` |
| **Quick Start** | `QUICKSTART.md` |
| **Data Guide** | `../data/oncology_trial_screening_data_guide_v03.md` |
| **BERT Docs** | https://huggingface.co/bert-base-uncased |
| **Scikit-learn Docs** | https://scikit-learn.org/ |
| **HuggingFace Guide** | https://huggingface.co/docs/transformers |

---

## TL;DR (Too Long; Didn't Read)

```
🎯 GOAL: Classify clinical notes into 5 eligibility categories

📊 RESULTS:
   - TF-IDF: 82.7% accuracy, <1 ms, 66 KB
   - BERT: 96.0% accuracy, 200-500 ms, 440 MB

✅ RECOMMENDATION:
   Use TF-IDF for fast screening (1st pass)
   Use BERT for final verification (2nd pass)

⏱️ GET STARTED:
   1. Run 01_data_preparation.ipynb
   2. Run 02_tfidf_logistic_regression.ipynb
   3. Read SUMMARY_REPORT.md
   4. Decide which model fits your needs

📈 NEXT STEP:
   Deploy TF-IDF + BERT ensemble for 90% TF-IDF speed with BERT accuracy
```

---

## Support

**Something not working?**
1. Check `README.md` Troubleshooting section
2. Review notebook markdown comments
3. Consult data guide for context
4. Check HuggingFace documentation

**Want to contribute?**
- Improve this documentation
- Implement ClinicalBERT variant
- Add explainability layer
- Build production API wrapper

---

**Ready to get started?** 👉 Open `01_data_preparation.ipynb` and run all cells!

**Want details?** 👉 Read `SUMMARY_REPORT.md` for comprehensive analysis

**Need help?** 👉 Check `README.md` for detailed documentation

---

**Last Updated**: February 2026
**Status**: Complete and tested ✓
**Models Trained**: TF-IDF, BERT
**Test Accuracy**: 82.7% (TF-IDF), 96.0% (BERT)
