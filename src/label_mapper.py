import pandas as pd

DATA_PATH = "data/processed/movement_clean.csv"
OUTPUT_PATH = "data/processed/movement_behavior.csv"

LABEL_COLUMN = "Position"

POSITION_TO_BEHAVIOR = {
    "lying": "Calm",
    "lying down": "Calm",
    "sitting": "Calm",

    "standing": "Active",
    "walking": "Active",

    "running": "Aggressive",
    "body shake": "Aggressive"
}


df = pd.read_csv(DATA_PATH)

if LABEL_COLUMN not in df.columns:
    raise ValueError(f"No '{LABEL_COLUMN}' column found")

df["behavior"] = df[LABEL_COLUMN].str.lower().map(POSITION_TO_BEHAVIOR)

if df["behavior"].isnull().any():
    unmapped = df[df["behavior"].isnull()][LABEL_COLUMN].unique()
    raise ValueError(f"Unmapped positions found: {unmapped}")

df.to_csv(OUTPUT_PATH, index=False)

print("✅ Position → Behavior mapping completed")
print(df["behavior"].value_counts())
