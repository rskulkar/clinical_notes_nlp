#!/usr/bin/env python3
"""Verify that data leakage removal works correctly."""

import pandas as pd
import numpy as np
import re
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, classification_report

def preprocess_text(text):
    """Preprocess clinical text."""
    if not isinstance(text, str):
        return ''
    text = text.lower()
    text = re.sub(r'\b\d+\.?\d*\b', '', text)
    text = re.sub(r'[^a-zA-Z\s\-]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# Load data
train_data = pd.read_csv('train_data.csv')
val_data = pd.read_csv('validation_data.csv')
test_data = pd.read_csv('test_data.csv')

print("="*70)
print("ORIGINAL DATA")
print("="*70)
print(f"Train: {len(train_data)}, Val: {len(val_data)}, Test: {len(test_data)}")

# Preprocess all texts
train_texts = [preprocess_text(text) for text in train_data['free_text_note']]
val_texts = [preprocess_text(text) for text in val_data['free_text_note']]
test_texts = [preprocess_text(text) for text in test_data['free_text_note']]

# Find leakage
test_texts_set = set(test_texts)
val_texts_set = set(val_texts)
train_test_overlap = [i for i, text in enumerate(train_texts) if text in test_texts_set]
train_val_overlap = [i for i, text in enumerate(train_texts) if text in val_texts_set]
overlap_indices = list(set(train_test_overlap + train_val_overlap))

print(f"\nLeakage detected:")
print(f"  Train samples in test: {len(train_test_overlap)}")
print(f"  Train samples in val: {len(train_val_overlap)}")
print(f"  Total to remove: {len(overlap_indices)}")

# Remove leakage
train_data_clean = train_data.drop(overlap_indices).reset_index(drop=True)
train_texts_clean = [preprocess_text(text) for text in train_data_clean['free_text_note']]

print("\n" + "="*70)
print("CLEANED DATA")
print("="*70)
print(f"Train: {len(train_data_clean)}, Val: {len(val_data)}, Test: {len(test_data)}")
print(f"Removed: {len(train_data) - len(train_data_clean)} samples")

print(f"\nClass distribution after cleaning:")
print(f"Train: {dict(Counter(train_data_clean['STATUS']))}")
print(f"Val:   {dict(Counter(val_data['STATUS']))}")
print(f"Test:  {dict(Counter(test_data['STATUS']))}")

# Train model on clean data
print("\n" + "="*70)
print("TRAINING MODEL ON CLEAN DATA")
print("="*70)

tfidf = TfidfVectorizer(max_features=5000, min_df=2, max_df=0.95,
                        ngram_range=(1, 2), stop_words='english',
                        lowercase=True, sublinear_tf=True)

X_train = tfidf.fit_transform(train_texts_clean)
X_val = tfidf.transform(val_texts)
X_test = tfidf.transform(test_texts)

y_train = train_data_clean['STATUS'].values
y_val = val_data['STATUS'].values
y_test = test_data['STATUS'].values

# Train logistic regression
lr = LogisticRegression(max_iter=1000, solver='lbfgs', random_state=42)
lr.fit(X_train, y_train)

# Evaluate
y_train_pred = lr.predict(X_train)
y_val_pred = lr.predict(X_val)
y_test_pred = lr.predict(X_test)

print("\n" + "="*70)
print("PERFORMANCE METRICS (CLEAN DATA)")
print("="*70)

results = {
    'Set': ['Train', 'Validation', 'Test'],
    'Accuracy': [],
    'Weighted F1': [],
    'Macro F1': []
}

for y_true, y_pred, set_name in [(y_train, y_train_pred, 'Train'),
                                  (y_val, y_val_pred, 'Validation'),
                                  (y_test, y_test_pred, 'Test')]:
    acc = accuracy_score(y_true, y_pred)
    wf1 = f1_score(y_true, y_pred, average='weighted', zero_division=0)
    mf1 = f1_score(y_true, y_pred, average='macro', zero_division=0)

    results['Accuracy'].append(acc)
    results['Weighted F1'].append(wf1)
    results['Macro F1'].append(mf1)

    print(f"\n{set_name} Set:")
    print(f"  Accuracy   : {acc:.4f}")
    print(f"  Weighted F1: {wf1:.4f}")
    print(f"  Macro F1   : {mf1:.4f}")

# Summary table
import pandas as pd
summary = pd.DataFrame(results)
print("\n" + "="*70)
print("SUMMARY TABLE")
print("="*70)
print(summary.to_string(index=False))

print("\n✓ Leakage fix verification complete!")
