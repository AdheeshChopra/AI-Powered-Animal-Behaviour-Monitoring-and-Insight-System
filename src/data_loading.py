# src/data_loading.py
import os
import glob
import pandas as pd
import librosa

# Attempt to download the movement dataset via Kaggle API
def download_movement_data():
    """
    Download the dog movement dataset (accelerometer/gyro) from Kaggle and unzip to data/raw.
    Requires Kaggle API credentials (set KAGGLE_USERNAME/KAGGLE_KEY or kaggle.json).
    """
    try:
        from kaggle.api.kaggle_api_extended import KaggleApi
        api = KaggleApi()
        api.authenticate()
        # Note: replace with the actual Kaggle dataset identifier
        dataset = 'benjamingray44/inertial-data-for-dog-behaviour-classification'
        api.dataset_download_files(dataset, path='data/raw/movement', unzip=True)
        print("Movement dataset downloaded.")
    except Exception as e:
        print("Failed to download movement data. Ensure Kaggle API is installed and credentials are set.")
        print(e)

# Load movement (accelerometer/gyro) data from raw CSV files into a single DataFrame
def load_movement_data():
    """
    Load all CSV files in data/raw/movement/ into a single pandas DataFrame.
    Assumes each CSV has columns like ['timestamp','acc_x','acc_y','acc_z','gyro_x','gyro_y','gyro_z','behavior'].
    """
    all_files = glob.glob('data/raw/movement/*.csv')
    if not all_files:
        raise FileNotFoundError("No movement CSV files found in data/raw/movement/")
    df_list = []
    for file in all_files:
        df = pd.read_csv(file)
        df_list.append(df)
    combined = pd.concat(df_list, ignore_index=True)
    print(f"Loaded {len(combined)} rows of movement data.")
    return combined

# (Optional) Download audio dataset. Here we assume user downloads the ZIP from Kaggle or hyper.ai.
def download_audio_data():
    """
    Placeholder for audio dataset download. 
    For example, use Kaggle API or direct download instructions to get audio-cats-and-dogs.zip into data/raw/audio/.
    """
    # e.g., using Kaggle API:
    # api.dataset_download_files('mmoreaux/audio-cats-and-dogs', path='data/raw', unzip=True)
    print("Please download the audio dataset (e.g. from Kaggle or http) into data/raw/audio/")

# Load audio files (WAV) into a list of (signal, sr) tuples
def load_audio_data():
    """
    Load all WAV audio files in data/raw/audio/ directory.
    Returns a list of tuples: [(y1, sr1), (y2, sr2), ...].
    """
    audio_files = glob.glob('data/raw/audio/*.wav')
    if not audio_files:
        raise FileNotFoundError("No audio files found in data/raw/audio/")
    audio_data = []
    for file in audio_files:
        y, sr = librosa.load(file, sr=None)  # load at native sample rate
        audio_data.append((y, sr))
    print(f"Loaded {len(audio_data)} audio files.")
    return audio_data
