import pandas as pd
import time
import joblib
import numpy as np
import os
from scipy.stats import skew, kurtosis

DATA_PATH = "data/processed/movement_clean.csv"
MODEL_PATH = "models/movement_rf_model.pkl"

# Load model
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Model not found at {MODEL_PATH}. Please run modeling.py first.")

model = joblib.load(MODEL_PATH)

# Load clean movement data
df = pd.read_csv(DATA_PATH)
sensor_cols = [col for col in df.columns if any(x in col for x in ['Acc', 'Gyr', 'Mag'])]

def extract_features(window):
    features = {}
    for col in sensor_cols:
        values = window[col].values
        features[col + '_mean'] = np.mean(values)
        features[col + '_std'] = np.std(values)
        features[col + '_min'] = np.min(values)
        features[col + '_max'] = np.max(values)
        features[col + '_skew'] = skew(values)
        features[col + '_kurtosis'] = kurtosis(values)
    return pd.DataFrame([features])

def simulate_real_time(interval=1.0, window_size=50):
    print("[✔] Starting simulated live classification...")
    for i in range(0, len(df) - window_size, window_size):
        window = df.iloc[i:i+window_size]
        features = extract_features(window)
        prediction = model.predict(features)[0]
        print(f"Live Prediction: {prediction}")
        time.sleep(interval)

if __name__ == '__main__':
    simulate_real_time(interval=0.5)
