#!/bin/bash

# Google Colab Setup Script for Clinical Notes Classification
# This script installs all required dependencies and mounts Google Drive

echo "======================================"
echo "Clinical Notes Classification - Colab Setup"
echo "======================================"

# Mount Google Drive
echo ""
echo "Step 1: Mounting Google Drive..."
# Note: In Colab, use: from google.colab import drive; drive.mount('/content/drive')

# Install dependencies
echo ""
echo "Step 2: Installing Python dependencies..."
pip install --quiet --upgrade pip
pip install --quiet pandas>=1.3.0
pip install --quiet numpy>=1.21.0
pip install --quiet matplotlib>=3.4.0
pip install --quiet seaborn>=0.11.0
pip install --quiet scikit-learn>=0.24.0
pip install --quiet torch>=1.9.0
pip install --quiet transformers>=4.10.0
pip install --quiet tokenizers>=0.12.0

echo ""
echo "Step 3: Verifying installations..."
python3 << END
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_extraction.text import TfidfVectorizer
import torch
from transformers import BertTokenizer

print("✓ pandas:", pd.__version__)
print("✓ numpy:", np.__version__)
print("✓ matplotlib:", plt.matplotlib.__version__)
print("✓ seaborn:", sns.__version__)
print("✓ torch:", torch.__version__)
print("✓ transformers installed")
print("✓ All dependencies successfully installed!")
END

echo ""
echo "======================================"
echo "Setup Complete!"
echo "======================================"
echo ""
echo "Next steps:"
echo "1. Change to working directory: %cd '/content/drive/My Drive/clinical_notes_classification/code'"
echo "2. Verify data file: !ls '../data/'"
echo "3. Start with notebook: 01_data_preparation.ipynb"
echo ""
