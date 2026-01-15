import pandas as pd
import numpy as np
import os
from scipy.stats import skew, kurtosis

INPUT_PATH = "data/processed/movement_clean.csv"
OUTPUT_PATH = "data/processed/movement_features.csv"

# Load cleaned data
df = pd.read_csv(INPUT_PATH)

# Identify sensor columns
sensor_cols = [col for col in df.columns if any(x in col for x in ['Acc', 'Gyr', 'Mag'])]

# Group by window (here simulated using Subject and Position for simplicity)
grouped = df.groupby(['Subject', 'Position'])

feature_rows = []
for (subject, position), group in grouped:
    feature_dict = {
        'Subject': subject,
        'Position': position
    }
    for col in sensor_cols:
        values = group[col].values
        feature_dict[col + '_mean'] = np.mean(values)
        feature_dict[col + '_std'] = np.std(values)
        feature_dict[col + '_min'] = np.min(values)
        feature_dict[col + '_max'] = np.max(values)
        feature_dict[col + '_skew'] = skew(values)
        feature_dict[col + '_kurtosis'] = kurtosis(values)

    feature_rows.append(feature_dict)

# Create dataframe
features_df = pd.DataFrame(feature_rows)

# Encode target label
features_df['Position'] = features_df['Position'].astype('category')
features_df['label'] = features_df['Position'].cat.codes

# Save to CSV
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
features_df.to_csv(OUTPUT_PATH, index=False)
print(f"[✔] Features saved to {OUTPUT_PATH}")