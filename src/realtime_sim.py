import pandas as pd
import numpy as np
import time
import joblib
import os
from scipy.stats import skew, kurtosis

# =====================================================
# Paths (project-root safe)
# =====================================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MOVEMENT_PATH = os.path.join(BASE_DIR, "data", "processed", "movement_clean.csv")
AUDIO_PATH = os.path.join(BASE_DIR, "data", "processed", "audio_features.csv")
MODEL_PATH = os.path.join(BASE_DIR, "models", "multimodal_rf_model.pkl")

# =====================================================
# Label maps
# =====================================================
LABEL_TO_POSITION = {
    0: "lying",
    1: "sitting",
    2: "walking",
    3: "standing",
    4: "body shake",
    5: "running"
}

LABEL_TO_BEHAVIOR = {
    "lying": "Calm",
    "sitting": "Calm",
    "standing": "Active",
    "walking": "Active",
    "running": "Aggressive",
    "body shake": "Aggressive"
}

# =====================================================
# Load model
# =====================================================
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError("❌ Multimodal model not found. Train first.")

model = joblib.load(MODEL_PATH)

# =====================================================
# Load datasets
# =====================================================
df_motion = pd.read_csv(MOVEMENT_PATH)
df_audio = pd.read_csv(AUDIO_PATH)

# Select IMU columns
sensor_cols = [
    col for col in df_motion.columns
    if any(x in col for x in ["Acc", "Gyr", "Mag"])
]

audio_feature_cols = [c for c in df_audio.columns if c != "File"]

# =====================================================
# Feature extraction (movement)
# =====================================================
def extract_motion_features(window):
    features = {}
    for col in sensor_cols:
        values = window[col].values
        features[col + "_mean"] = np.mean(values)
        features[col + "_std"] = np.std(values)
        features[col + "_min"] = np.min(values)
        features[col + "_max"] = np.max(values)
        features[col + "_skew"] = skew(values)
        features[col + "_kurtosis"] = kurtosis(values)
    return features

# =====================================================
# Real-time multimodal simulation
# =====================================================
def simulate_realtime(interval=0.5, window_size=50):
    print("🚀 Starting MULTIMODAL real-time simulation...\n")

    audio_idx = 0

    for i in range(0, len(df_motion) - window_size, window_size):
        # Movement window
        motion_window = df_motion.iloc[i:i + window_size]
        motion_feats = extract_motion_features(motion_window)

        # Audio sample (cyclic)
        audio_row = df_audio.iloc[audio_idx % len(df_audio)]
        audio_feats = audio_row[audio_feature_cols].to_dict()
        audio_idx += 1

        # Combine features
        combined = {**motion_feats, **audio_feats}
        X = pd.DataFrame([combined]).fillna(0)

        # Predict
        pred = model.predict(X)[0]
        position = LABEL_TO_POSITION.get(pred, "Unknown")
        behavior = LABEL_TO_BEHAVIOR.get(position, "Unknown")

        print(f"🐾 Behavior: {behavior:<10} | Posture: {position}")
        time.sleep(interval)

# =====================================================
if __name__ == "__main__":
    simulate_realtime()
