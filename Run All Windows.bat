@echo off

REM Activate virtual environment
call .venv\Scripts\activate

echo [1] Installing dependencies...
pip install -r requirements.txt

echo [2] Running preprocessing...
python src\preprocessing.py

echo [3] Extracting features...
python src\feature_extraction.py

echo [4] Training model...
python src\modeling.py

echo [5] Simulating real-time data...
python src\realtime_sim.py

echo [✔] All steps completed successfully.
echo [👉] To launch UI, run: streamlit run src\streamlit_app.py
pause
