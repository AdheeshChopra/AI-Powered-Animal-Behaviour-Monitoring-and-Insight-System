import pandas as pd
import os

MOVEMENT_FEATURES_PATH = "data/processed/movement_features.csv"
AUDIO_FEATURES_PATH = "data/processed/audio_features.csv"
MERGED_OUTPUT_PATH = "data/processed/merged_features.csv"

# -------------------------------
# Load datasets
# -------------------------------
df_movement = pd.read_csv(MOVEMENT_FEATURES_PATH)
df_audio = pd.read_csv(AUDIO_FEATURES_PATH)

print("📄 Movement rows:", len(df_movement))
print("🎵 Audio rows:", len(df_audio))

# -------------------------------
# Normalize key column
# -------------------------------
if "Subject" in df_movement.columns:
    df_movement.rename(columns={"Subject": "File"}, inplace=True)

# -------------------------------
# Remove duplicate audio rows per file
# (VERY IMPORTANT)
# -------------------------------
df_audio = df_audio.groupby("File").mean(numeric_only=True).reset_index()

# -------------------------------
# Merge (broadcast audio → movement)
# -------------------------------
df_combined = df_movement.merge(df_audio, on="File", how="left")

# -------------------------------
# Handle missing audio safely
# -------------------------------
df_combined.fillna(0, inplace=True)

# -------------------------------
# Safety check
# -------------------------------
if len(df_combined) == 0:
    raise RuntimeError("❌ Merge resulted in ZERO rows")

# -------------------------------
# Save
# -------------------------------
os.makedirs(os.path.dirname(MERGED_OUTPUT_PATH), exist_ok=True)
df_combined.to_csv(MERGED_OUTPUT_PATH, index=False)

print(f"✅ Merged dataset saved → {MERGED_OUTPUT_PATH}")
print("📊 Final shape:", df_combined.shape)
