import pandas as pd
import os

# Paths
RAW_DATA_PATH = "data/raw/movement/df_raw.csv"
DOGS_DATA_PATH = "data/raw/movement/df_dogs.csv"
OUTPUT_DIR = "data/processed"
OUTPUT_FILE = "movement_clean.csv"
OUTPUT_PATH = os.path.join(OUTPUT_DIR, OUTPUT_FILE)

# Load data
df_raw = pd.read_csv(RAW_DATA_PATH)
df_dogs = pd.read_csv(DOGS_DATA_PATH)

# Merge dog metadata
df = df_raw.merge(df_dogs, on=["Subject", "Breed"], how="left")

# Drop rows with missing critical values (e.g., sensor or target labels)
sensor_cols = [col for col in df.columns if any(sensor in col for sensor in ["Acc", "Gyr", "Mag"])]
target_cols = ['Type', 'Position']
df.dropna(subset=sensor_cols + target_cols, inplace=True)

# Encode categorical labels
df['Type'] = df['Type'].astype('category')
df['Position'] = df['Position'].astype('category')
df['Type_code'] = df['Type'].cat.codes
df['Position_code'] = df['Position'].cat.codes

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Save processed file
df.to_csv(OUTPUT_PATH, index=False)
print(f"[✔] Processed data saved to {OUTPUT_PATH}")
