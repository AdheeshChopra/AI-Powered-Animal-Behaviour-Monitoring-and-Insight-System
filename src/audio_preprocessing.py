import os
import pandas as pd
import librosa
import numpy as np

# =====================================================
# Resolve project root safely
# =====================================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

AUDIO_DIR = os.path.join(BASE_DIR, "data", "raw", "audio")
OUTPUT_CSV = os.path.join(BASE_DIR, "data", "processed", "audio_features.csv")

SUPPORTED_EXT = (".wav", ".mp3", ".flac", ".ogg")

# =====================================================
# Feature extraction
# =====================================================
def extract_features(file_path):
    y, sr = librosa.load(file_path, sr=None)

    mfcc = np.mean(librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13).T, axis=0)
    chroma = np.mean(librosa.feature.chroma_stft(y=y, sr=sr).T, axis=0)
    contrast = np.mean(librosa.feature.spectral_contrast(y=y, sr=sr).T, axis=0)

    return np.hstack((mfcc, chroma, contrast))

# =====================================================
# Main
# =====================================================
def main():
    print("📁 AUDIO_DIR resolved to:", AUDIO_DIR)

    if not os.path.exists(AUDIO_DIR):
        raise FileNotFoundError(f"❌ Audio directory not found: {AUDIO_DIR}")

    rows = []
    audio_count = 0

    # 🔑 RECURSIVE WALK (THIS IS THE FIX)
    for root, _, files in os.walk(AUDIO_DIR):
        for fname in files:
            if fname.lower().endswith(SUPPORTED_EXT):
                audio_count += 1
                path = os.path.join(root, fname)

                try:
                    features = extract_features(path)

                    # Use filename WITHOUT extension
                    file_id = os.path.splitext(fname)[0]

                    rows.append([file_id] + list(features))

                except Exception as e:
                    print(f"❌ Failed on {fname}: {e}")

    print(f"🎵 Found {audio_count} audio files")

    columns = (
        ["File"]
        + [f"mfcc_{i}" for i in range(13)]
        + [f"chroma_{i}" for i in range(12)]
        + [f"contrast_{i}" for i in range(7)]
    )

    df = pd.DataFrame(rows, columns=columns)

    os.makedirs(os.path.dirname(OUTPUT_CSV), exist_ok=True)
    df.to_csv(OUTPUT_CSV, index=False)

    print(f"✅ Audio features saved → {OUTPUT_CSV}")
    print("📊 Audio feature shape:", df.shape)

# =====================================================
if __name__ == "__main__":
    main()