# AI-EnergyForcastR4
AI-Driven Predictive Maintenance for Renewable Energy Assets 
# AI-Driven Predictive Maintenance for Renewable Energy Assets

This project develops a cross-platform application for predictive maintenance of renewable energy assets (wind turbines, solar panels, inverters, batteries). It uses IoT sensor data, external weather/solar APIs, and AI/ML models to forecast failures and optimize maintenance schedules.

---

## 🚀 Features
- Real-time sensor data ingestion (temperature, humidity, irradiance, wind speed).
- External API integration (OpenWeather, NASA POWER, Tomorrow.io).
- Local PostgreSQL + TimescaleDB storage for time-series data.
- Preprocessing scripts for normalization, cleaning, and interpolation.
- Ready for deployment on Raspberry Pi 4, but fully compatible with Mac and Windows laptops during development.

---

## 🛠️ Development Setup

### 1. Clone Repository
```bash
AI-EnergyForcastR4/
│
├── db/                     # Database setup and connectors
│   ├── db_connector.py     # Python script to handles DB connection
│   ├── db_ingest.py        # Python script to ingestion script (imports connector)
│   ├── test_connection.py  # Python script for quick connection test
│   └── schema.sql          # SQL table definitions
│
├── data/                 
│   ├── sensor_logs.txt   # plain text log file 
│   └── sensor_data.csv   # CSV file 
│
├── .env
├── requirements.txt      # List of Python dependencies
├── README.md             # Documentation for setup and usage
├── logs/
│   └── ingestion.log         # today’s log)
│   └── ingestion.log.2026-01-20  #yesterday’s log, auto‑created at midnight
│
├── sensors/              # Scripts for sensor data (real or simulated)
│   └── sensor_ingest.py  # First script: generate or simulate sensor readings
│
├── api_wrappers/         # External API modules
│   └── openweather.py    # First wrapper: fetch weather data
│   └── nasa_power.py     # Second wrapper: fetch solar/irradiance data
│
│
├── preprocessing/        # Data cleaning scripts
│   └── preprocess.py     # First script: normalize and clean sensor logs
│
└── notebooks/            # Jupyter notebooks for demos
    └── data_pipeline_demo.ipynb  # Step-by-step interactive demo

#### my notes
'''bash
Perfect 🎉 — that package list shows your environment is now fully set up and healthy. You’ve got all the core libraries installed:
requests → API calls and HTTP requests
pandas → data handling and analysis
numpy → numerical computations
psycopg2-binary → PostgreSQL connector
scikit-learn → classical machine learning models
torch → PyTorch deep learning framework
matplotlib → static plotting
plotly → interactive charts
paho-mqtt → IoT sensor communication
Plus all their dependencies (like scipy, joblib, threadpoolctl, etc.). This means you’re ready to start coding your actual project.
PS D:\My Documents\tools\skul\bsu2024\bsu_mot512_thesis1\GithubVisualStudioCode\AI-EnergyForcastR4> python -m pip list
Package            Version
------------------ -----------
certifi            2026.1.4
charset-normalizer 3.4.4
contourpy          1.3.3
cycler             0.12.1
filelock           3.20.3
fonttools          4.61.1
fsspec             2026.1.0
idna               3.11
Jinja2             3.1.6
joblib             1.5.3
kiwisolver         1.4.9
MarkupSafe         3.0.3
matplotlib         3.10.8
mpmath             1.3.0
narwhals           2.15.0
networkx           3.6.1
numpy              2.4.1
packaging          25.0
paho-mqtt          2.1.0
pandas             2.3.3
pillow             12.1.0
pip                25.3
plotly             6.5.2
psycopg2-binary    2.9.11
pyparsing          3.3.1
python-dateutil    2.9.0.post0
pytz               2025.2
requests           2.32.5
scikit-learn       1.8.0
scipy              1.17.0
setuptools         80.9.0
six                1.17.0
sympy              1.14.0
threadpoolctl      3.6.0
torch              2.9.1
typing_extensions  4.15.0
tzdata             2025.3
urllib3            2.6.3

[always used for activating env; "venv\Scripts\activate.bat"]
[This starts PostgreSQL in the background, listening on port 5432.
Since you don’t have admin rights, it won’t be a Windows service — you’ll need to run this manually each time.
in <cmd> <"D:\My Documents\tools\postgresql\pgsql\bin\pg_ctl.exe" -D "D:\My Documents\tools\postgresql\pgsql\data" -l logfile start>]
[Stopping PostgreSQL. When you’re done, stop the server cleanly, This shuts down PostgreSQL safely:
in cmd> <"D:\My Documents\tools\postgresql\pgsql\bin\pg_ctl.exe" -D "D:\My Documents\tools\postgresql\pgsql\data" stop>]
[Restarting PostgreSQL, If you want to restart:
in cmd> <"D:\My Documents\tools\postgresql\pgsql\bin\pg_ctl.exe" -D "D:\My Documents\tools\postgresql\pgsql\data" restart>]

...notes 260119;
Phase,Item,Status
Phase 1: Environment Setup,Install PostgreSQL portable binaries,Done
Phase 1: Environment Setup,Initialize database cluster (initdb),Done
Phase 1: Environment Setup,Start PostgreSQL manually (pg_ctl),Done
Phase 1: Environment Setup,Connect with psql,Done
Phase 2: Database Schema,Create energy_db database,Done
Phase 2: Database Schema,Define sensor_data table schema,Done
Phase 2: Database Schema,Verify schema with \d sensor_data,Done
Phase 3: Python Integration,Install psycopg2 driver,Done
Phase 3: Python Integration,Create db_ingest.py script,Done
Phase 3: Python Integration,Connect Python to PostgreSQL,Done
Phase 3: Python Integration,Insert test row via Python,Done
Phase 3: Python Integration,Fetch and display rows via Python,Done
Phase 4: Log Ingestion,Adapt script to read sensor_logs.txt,Done
Phase 4: Log Ingestion,Insert multiple rows from file,Done
Phase 4: Log Ingestion,Verify ingestion with query output,Done
Phase 5: Enhancements,Handle duplicate entries (unique timestamp + ON CONFLICT),Pending
Phase 5: Enhancements,Format timestamp output (seconds only),Done
Phase 5: Enhancements,Optional: pretty table output,Pending
Phase 6: Next Steps,Automate ingestion (batch file or cron job),Pending
Phase 6: Next Steps,Extend ingestion for CSV/real sensor streams,Pending
Phase 6: Next Steps,Dashboard/visualization integration,Pending
...notes 260120;
sql password = PdM
Phase 1: Environment Setup
Install PostgreSQL portable binaries → Done
Initialize database cluster (initdb) → Done
Start PostgreSQL manually (pg_ctl) → Done
Connect with psql → Done
Phase 2: Database Schema
Create energy_db database → Done
Define sensor_data table schema → Done
Verify schema with \d sensor_data → Done
Phase 3: Python Integration
Install psycopg2 driver → Done
Create db_ingest.py script → Done
Connect Python to PostgreSQL → Done
Insert test row via Python → Done
Fetch and display rows via Python → Done
Phase 4: Log Ingestion
Adapt script to read sensor_logs.txt → Done
Insert multiple rows from file → Done
Verify ingestion with query output → Done
Phase 5 Completion Checklist
Format timestamp output (seconds only) → Done
Pretty table output → Done
Row count before/after ingestion → Done
Skip header line in text ingestion → Done
Modularize connection (db_connector.py) → Done
Add test script (test_connection.py) → Done
Show top/bottom rows in test script → Done
Handle duplicate entries (unique timestamp + ON CONFLICT) → Done 
Phase 6: Next Steps
Automate ingestion (batch file or cron job) → Pending
Extend ingestion for CSV/real sensor streams → Pending
Dashboard/visualization integration → Pending
Add permanent log file output (logs/ingestion.log) → Pending
...phase6
Step 2:Windows Batch File (simple automation)
    Open Notepad.
    Paste this:
        bat
        @echo off
        cd /d "D:\My Documents\tools\skul\bsu2024\bsu_mot512_thesis1\GithubVisualStudioCode\AI-EnergyForcastR4"
        python db\db_ingest.py
    Save as run_ingest.bat in your repo root.
    Double‑click it → ingestion runs, logs go to logs/ingestion.log.
Step 3: Schedule with Task Scheduler
    Open Task Scheduler (Windows search).
    Create a new task → “Run Ingestion Daily”.
    Set trigger → e.g., every day at 8:00 AM.
    Set action → run run_ingest.bat.
    Save → ingestion now runs automatically.