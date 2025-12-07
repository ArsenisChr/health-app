# -*- coding: utf-8 -*-
"""
Lifestyle Cluster Training Script (XGBoost)
"""

import pandas as pd
import joblib
from sklearn.cluster import AgglomerativeClustering
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report
from xgboost import XGBClassifier
import gower
import matplotlib.pyplot as plt

# ---------------------------------------------------------
# 1. LOAD & PREPROCESS DATASET
# ---------------------------------------------------------
# Update path to your local dataset
csv_path = r"clustered_with_labels.csv"
print(f"Loading dataset from: {csv_path}")

df = pd.read_csv(csv_path)

# Clean up
df = df.reset_index(drop=True)
df = df.loc[:, ~df.columns.str.contains("^Unnamed")]

print("Dataset shape:", df.shape)

# ---------------------------------------------------------
# 3. TRAIN CLASSIFIER (XGBoost)
# ---------------------------------------------------------
print("\nPreparing for XGBoost training...")

# Features to DROP for training (Target + Non-predictive IDs)
drop_cols_model = ["lifestyle_cluster", "cluster", "Gender", "Πόλη", 'Interest', 'disorders', 'Diagnosis']
# If you created PC1/PC2 earlier, drop them too
drop_cols_model.extend(["PC1", "PC2"])

df_model = df.drop(columns=drop_cols_model, errors="ignore")
X = df_model
y = df["lifestyle_cluster"]

# One-Hot Encoding for categorical features
X = pd.get_dummies(X, drop_first=True)

# Encode Target
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

# Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
)

# Initialize & Train XGBoost
model = XGBClassifier(
    n_estimators=300,
    max_depth=6,
    learning_rate=0.05,
    subsample=0.9,
    colsample_bytree=0.9,
    objective="multi:softmax",
    num_class=len(label_encoder.classes_),
    random_state=42
)

print("Training XGBoost...")
model.fit(X_train, y_train)

# Evaluation
y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)
print(f"\nAccuracy: {acc:.4f}")
print("\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=label_encoder.classes_))

# ---------------------------------------------------------
# 4. EXPORT MODEL & ARTIFACTS
# ---------------------------------------------------------
print("\nExporting model artifacts...")

# 1. Save XGBoost Model
model.save_model("xgb_lifestyle_model.json")
print("- Model saved: xgb_lifestyle_model.json")

# 2. Save Label Encoder (to decode 0,1,2 -> 'Couch Potato')
joblib.dump(label_encoder, "label_encoder.pkl")
print("- Label Encoder saved: label_encoder.pkl")

# 3. Save Feature Names (to ensure input data has same columns in same order)
feature_names = X_train.columns.tolist()
joblib.dump(feature_names, "feature_names.pkl")
print("- Feature Names saved: feature_names.pkl")

print("\nDone! Copy these 3 files to your backend application folder.")
