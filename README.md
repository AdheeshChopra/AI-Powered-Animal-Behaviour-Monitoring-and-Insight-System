<<<<<<< HEAD
# 🐾 Canine Dog Behavior Monitoring with AI + Wearable Sensors

**Canine Behaviour ML** is a low-cost, AI-powered system that analyzes dog behavior using motion, sound, and temperature data. It classifies activities like walking, sitting, barking, and resting using machine learning—and it's designed to run on both laptops and wearable devices like the ESP32.

Built for affordability, real-world deployment, and the Indian context, PawSense-AI uses **public datasets** to train its models and supports **sensor integration** for future expansion.

---

## 🎯 Features

- 🧠 Behavior classification using AI (Random Forest)
- 📊 Works with motion (IMU), temperature, and sound data
- 🔌 Sensor-ready (ESP32 + MPU6050 + Temp Sensor)
- 🖥️ Real-time simulation with live predictions
- 📈 Streamlit dashboard for interactive behavior monitoring
- 📦 Modular, well-documented, beginner-friendly codebase

---

## 🗂️ Project Structure

pawsense-ai/
├── data/ # Raw + processed datasets
│ ├── raw/
│ └── processed/
├── src/ # Core Python modules
│ ├── data_loading.py
│ ├── preprocessing.py
│ ├── feature_extraction.py
│ ├── modeling.py
│ ├── realtime_sim.py
│ ├── streamlit_app.py
│ └── sensor_integration.py
├── arduino/ # Sensor-side C++ code
│ └── imu_temp_sensor.ino
├── requirements.txt
└── README.md

---

## 📚 Datasets Used

| Type      | Dataset                                                                 |
|-----------|--------------------------------------------------------------------------|
| Motion    | [Dog Movement Sensor Dataset (Mendeley)](https://data.mendeley.com/datasets/vxhx934tbn/1)  
| Audio     | [UrbanSound8K](https://urbansounddataset.weebly.com/urbansound8k.html)  
| Posture   | [Dog Posture Recognition Dataset](https://data.mendeley.com/datasets/mpph6bmn7g/1)  
| Temp (simulated) | [Kaggle: Wearable Body Temp Dataset](https://www.kaggle.com/datasets/kukuroo3/smart-wearable-body-temperature-monitoring)  

---

## ⚙️ Getting Started

### 1. Install Dependencies

pip install -r requirements.txt

python src/data_loading.py
python src/preprocessing.py
python src/feature_extraction.py
python src/modeling.py

### 2. Download Datasets
Place CSV and audio files in data/raw/ as described in each dataset link above.

### 3. Run Full Pipeline
python src/data_loading.py
python src/preprocessing.py
python src/feature_extraction.py
python src/modeling.py

### 4. Real-Time Simulation
python src/realtime_sim.py

### 5. Streamlit Dashboard
streamlit run src/streamlit_app.py
=======
🐾 Canine Dog Behavior Monitoring with AI + Wearable Sensors
Canine Behaviour ML is a low-cost, AI-powered system that analyzes dog behavior using motion, sound, and temperature data. It classifies activities like walking, sitting, barking, and resting using machine learning—and it's designed to run on both laptops and wearable devices like the ESP32.

Built for affordability, real-world deployment, and the Indian context, PawSense-AI uses public datasets to train its models and supports sensor integration for future expansion.

🎯 Features
🧠 Behavior classification using AI (Random Forest)
📊 Works with motion (IMU), temperature, and sound data
🔌 Sensor-ready (ESP32 + MPU6050 + Temp Sensor)
🖥️ Real-time simulation with live predictions
📈 Streamlit dashboard for interactive behavior monitoring
📦 Modular, well-documented, beginner-friendly codebase
🗂️ Project Structure
pawsense-ai/ ├── data/ # Raw + processed datasets │ ├── raw/ │ └── processed/ ├── src/ # Core Python modules │ ├── data_loading.py │ ├── preprocessing.py │ ├── feature_extraction.py │ ├── modeling.py │ ├── realtime_sim.py │ ├── streamlit_app.py │ └── sensor_integration.py ├── arduino/ # Sensor-side C++ code │ └── imu_temp_sensor.ino ├── requirements.txt └── README.md

📚 Datasets Used
Type	Dataset
Motion	Dog Movement Sensor Dataset (Mendeley)
Audio	UrbanSound8K
Posture	Dog Posture Recognition Dataset
Temp (simulated)	Kaggle: Wearable Body Temp Dataset
⚙️ Getting Started
1. Install Dependencies
pip install -r requirements.txt

python src/data_loading.py python src/preprocessing.py python src/feature_extraction.py python src/modeling.py

2. Download Datasets
Place CSV and audio files in data/raw/ as described in each dataset link above.

3. Run Full Pipeline
python src/data_loading.py python src/preprocessing.py python src/feature_extraction.py python src/modeling.py

4. Real-Time Simulation
python src/realtime_sim.py

5. Streamlit Dashboard
streamlit run src/streamlit_app.py
>>>>>>> 8f7b6dd (canine-behaviour-ml)
