import streamlit as st
import pandas as pd
import joblib
import numpy as np
import os
import time
from scipy.stats import skew, kurtosis

DATA_PATH = "data/processed/movement_clean.csv"
MODEL_PATH = "models/movement_rf_model.pkl"

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
    "lying down": "Calm",
    "sitting": "Calm",
    "standing": "Active",
    "walking": "Active",
    "running": "Aggressive",
    "body shake": "Aggressive"
}

st.set_page_config(page_title="Canine Behavior Classifier", layout="wide")
st.title("🐶 Behavior Classification Dashboard")

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)
    return df

df = load_data()
sensor_cols = [col for col in df.columns if any(x in col for x in ['Acc', 'Gyr', 'Mag'])]

# Load model
if not os.path.exists(MODEL_PATH):
    st.error(f"Model not found at {MODEL_PATH}. Please run modeling.py first.")
    st.stop()
model = joblib.load(MODEL_PATH)

# Feature extraction
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

# Sidebar controls
window_size = st.sidebar.slider("Select Window Size", 10, 100, 50, step=10)
step_size = st.sidebar.slider("Step Size", 10, 100, 50, step=10)
st.sidebar.markdown("---")
st.sidebar.markdown("Behaviour Analysis")

# Main simulation loop
st.subheader("Live Predictions")
placeholder = st.empty()

for i in range(0, len(df) - window_size, step_size):
    window = df.iloc[i:i + window_size]
    features = extract_features(window)
    prediction = model.predict(features)[0]
    position = LABEL_TO_POSITION.get(prediction, "Unknown")
    behavior = LABEL_TO_BEHAVIOR.get(position, "Unknown")

    with placeholder.container():
        st.markdown(f"### 🧠 Predicted Behavior: `{behavior}`")
        st.dataframe(window[sensor_cols].tail(5))
        time.sleep(0.5)
