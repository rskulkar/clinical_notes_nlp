#!/usr/bin/env python3
"""Deep investigation of why model gets perfect scores."""

import pandas as pd
import numpy as np
import re
from collections import Counter

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
print("INVESTIGATION: Why is performance perfect?")
print("="*70)

# Preprocess
train_texts = [preprocess_text(text) for text in train_data['free_text_note']]
val_texts = [preprocess_text(text) for text in val_data['free_text_note']]
test_texts = [preprocess_text(text) for text in test_data['free_text_note']]

# 1. Check if texts are too short/empty
print("\n1. TEXT LENGTH ANALYSIS")
print("-" * 70)
train_lengths = [len(t.split()) for t in train_texts]
val_lengths = [len(t.split()) for t in val_texts]
test_lengths = [len(t.split()) for t in test_texts]

print(f"Train - Mean: {np.mean(train_lengths):.1f}, Min: {min(train_lengths)}, Max: {max(train_lengths)}")
print(f"Val   - Mean: {np.mean(val_lengths):.1f}, Min: {min(val_lengths)}, Max: {max(val_lengths)}")
print(f"Test  - Mean: {np.mean(test_lengths):.1f}, Min: {min(test_lengths)}, Max: {max(test_lengths)}")

# 2. Check class imbalance
print("\n2. CLASS IMBALANCE")
print("-" * 70)
train_counts = Counter(train_data['STATUS'])
val_counts = Counter(val_data['STATUS'])
test_counts = Counter(test_data['STATUS'])

for cls in sorted(train_counts.keys()):
    pct_train = 100 * train_counts[cls] / len(train_data)
    pct_val = 100 * val_counts.get(cls, 0) / len(val_data)
    pct_test = 100 * test_counts.get(cls, 0) / len(test_data)
    print(f"{cls:15} Train: {pct_train:5.1f}%  Val: {pct_val:5.1f}%  Test: {pct_test:5.1f}%")

# 3. Check if a single class dominates
print("\n3. DOMINANT CLASS ANALYSIS")
print("-" * 70)
dominant_class = train_counts.most_common(1)[0][0]
dominant_pct = 100 * train_counts[dominant_class] / len(train_data)
print(f"Dominant class: {dominant_class} ({dominant_pct:.1f}%)")
print(f"If model predicts only {dominant_class}:")

from sklearn.metrics import accuracy_score
baseline_pred = np.full(len(test_data), dominant_class)
baseline_acc = accuracy_score(test_data['STATUS'], baseline_pred)
print(f"  Baseline accuracy on test: {baseline_acc:.4f}")

# 4. Check for duplicate texts within same class
print("\n4. DUPLICATE TEXT ANALYSIS")
print("-" * 70)
train_text_class = list(zip(train_texts, train_data['STATUS']))
unique_texts = len(set(train_texts))
print(f"Total train samples: {len(train_texts)}")
print(f"Unique preprocessed texts: {unique_texts}")
print(f"Duplicate texts: {len(train_texts) - unique_texts}")

# Check if duplicates are in the same class or different classes
dup_same_class = 0
dup_diff_class = 0
seen = {}
for text, status in train_text_class:
    if text in seen:
        if seen[text] == status:
            dup_same_class += 1
        else:
            dup_diff_class += 1
    else:
        seen[text] = status

print(f"Duplicates with same class: {dup_same_class}")
print(f"Duplicates with different classes: {dup_diff_class}")

if dup_diff_class > 0:
    print("\n⚠️  WARNING: Same text appears with DIFFERENT classes!")
    print("This makes the problem fundamentally ambiguous and might explain perfect scores.")

# 5. Text examples for each class
print("\n5. SAMPLE TEXTS BY CLASS")
print("-" * 70)
for status in sorted(train_data['STATUS'].unique()):
    idx = train_data[train_data['STATUS'] == status].index[0]
    text = train_texts[idx]
    print(f"\n{status}:")
    print(f"  Original: {train_data['free_text_note'].iloc[idx][:150]}")
    print(f"  Processed: {text[:150]}")

# 6. Check feature diversity
print("\n6. FEATURE DIVERSITY CHECK")
print("-" * 70)
from sklearn.feature_extraction.text import TfidfVectorizer

# Count unique unigrams per class
for status in sorted(train_data['STATUS'].unique()):
    status_texts = [train_texts[i] for i in range(len(train_texts)) if train_data['STATUS'].iloc[i] == status]
    words = set()
    for text in status_texts:
        words.update(text.split())
    print(f"{status:15}: {len(words):4} unique words")

print("\n" + "="*70)
print("END INVESTIGATION")
print("="*70)
