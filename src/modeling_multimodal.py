import pandas as pd
import joblib
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from imblearn.over_sampling import SMOTE

MERGED_DATA_PATH = "data/processed/merged_features.csv"
MODEL_OUTPUT_PATH = "models/multimodal_rf_model.pkl"

# -------------------------------
# Load dataset
# -------------------------------
if not os.path.exists(MERGED_DATA_PATH):
    raise FileNotFoundError(f"❌ File not found: {MERGED_DATA_PATH}")

df = pd.read_csv(MERGED_DATA_PATH)
print("📑 Total columns:", len(df.columns))

# -------------------------------
# Label check
# -------------------------------
if "label" not in df.columns:
    raise ValueError("❌ 'label' column missing")

y = df["label"]

# -------------------------------
# Feature selection
# -------------------------------
drop_cols = ["File", "Position", "label"]
X = df.drop(columns=[c for c in drop_cols if c in df.columns])

# -------------------------------
# Convert ONLY object columns
# -------------------------------
object_cols = X.select_dtypes(include=["object"]).columns
X[object_cols] = X[object_cols].apply(pd.to_numeric, errors="coerce")

# -------------------------------
# Handle NaNs
# -------------------------------
X = X.fillna(X.median(numeric_only=True))

# -------------------------------
# Final sanity check
# -------------------------------
if X.shape[1] == 0:
    raise ValueError("❌ No features left after preprocessing")

print(f"✅ Final feature matrix: {X.shape}")
print("🎯 Label distribution:\n", y.value_counts())

# -------------------------------
# Balance dataset (SMOTE safe)
# -------------------------------
min_class_size = y.value_counts().min()
if min_class_size < 2:
    raise ValueError("❌ SMOTE requires at least 2 samples per class")

smote = SMOTE(random_state=42, k_neighbors=min(5, min_class_size - 1))
X_res, y_res = smote.fit_resample(X, y)

# -------------------------------
# Train / Test split
# -------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X_res, y_res, test_size=0.2, random_state=42, stratify=y_res
)

# -------------------------------
# Train model
# -------------------------------
model = RandomForestClassifier(
    n_estimators=300,
    max_depth=None,
    random_state=42,
    n_jobs=-1
)
model.fit(X_train, y_train)

# -------------------------------
# Evaluate
# -------------------------------
y_pred = model.predict(X_test)
print(f"\n✅ Accuracy: {accuracy_score(y_test, y_pred):.4f}")
print("📊 Classification Report:\n", classification_report(y_test, y_pred))

# -------------------------------
# Save model
# -------------------------------
os.makedirs(os.path.dirname(MODEL_OUTPUT_PATH), exist_ok=True)
joblib.dump(model, MODEL_OUTPUT_PATH)

print(f"💾 Model saved → {MODEL_OUTPUT_PATH}")
