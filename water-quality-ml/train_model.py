import os
import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, confusion_matrix, classification_report
)
from xgboost import XGBClassifier

# ─────────────────────────────────────────────
# 1. Load Dataset
# ─────────────────────────────────────────────
DATASET_PATH = os.path.join("dataset", "water_potability.csv")
MODEL_PATH   = os.path.join("models", "xgboost.sav")
SCALER_PATH  = os.path.join("models", "scaler.sav")

df = pd.read_csv(DATASET_PATH)

print(df.head())

# ─────────────────────────────────────────────
# 2. Data Preprocessing
# ─────────────────────────────────────────────
print("\n[INFO] Checking missing values...")
print(df.isnull().sum())

# Fill missing values with column medians
df.fillna(df.median(numeric_only=True), inplace=True)
print("[INFO] Missing values filled with median.")

# Features and target
FEATURES = ["ph", "Hardness", "Solids", "Chloramines",
            "Sulfate", "Conductivity", "Organic_carbon",
            "Trihalomethanes", "Turbidity"]
TARGET = "Potability"

X = df[FEATURES]
y = df[TARGET]
# ─────────────────────────────────────────────
# 3. Train / Test Split
# ─────────────────────────────────────────────
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
# ─────────────────────────────────────────────
# 4. Feature Scaling
# ─────────────────────────────────────────────
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled  = scaler.transform(X_test)
# ─────────────────────────────────────────────
# 5. Model Training
# ─────────────────────────────────────────────
model = XGBClassifier(
    n_estimators=300,
    max_depth=6,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    use_label_encoder=False,
    eval_metric="logloss",
    random_state=42
)
model.fit(X_train_scaled, y_train)
# ─────────────────────────────────────────────
# 6. Evaluation
# ─────────────────────────────────────────────
y_pred = model.predict(X_test_scaled)

acc  = accuracy_score(y_test, y_pred)
prec = precision_score(y_test, y_pred)
rec  = recall_score(y_test, y_pred)
f1   = f1_score(y_test, y_pred)

print("\n========== Model Performance ==========")
print(f"  Accuracy  : {acc:.4f}")
print(f"  Precision : {prec:.4f}")
print(f"  Recall    : {rec:.4f}")
print(f"  F1-Score  : {f1:.4f}")
print("\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=["Not Potable", "Potable"]))

# Confusion Matrix plot
cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(6, 5))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
            xticklabels=["Not Potable", "Potable"],
            yticklabels=["Not Potable", "Potable"])
plt.title("Confusion Matrix – Water Potability Prediction")
plt.ylabel("Actual")
plt.xlabel("Predicted")
plt.tight_layout()
plt.savefig(os.path.join("static", "confusion_matrix.png"), dpi=120)


# Feature Importance plot
plt.figure(figsize=(8, 5))
importance = pd.Series(model.feature_importances_, index=FEATURES)
importance.sort_values().plot(kind="barh", color="#4A90D9")
plt.title("XGBoost Feature Importances")
plt.xlabel("Importance Score")
plt.tight_layout()
plt.savefig(os.path.join("static", "feature_importance.png"), dpi=120)


# ─────────────────────────────────────────────
# 7. Save Model and Scaler
# ─────────────────────────────────────────────
os.makedirs("models", exist_ok=True)
pickle.dump(model,  open(MODEL_PATH,  "wb"))
pickle.dump(scaler, open(SCALER_PATH, "wb"))

