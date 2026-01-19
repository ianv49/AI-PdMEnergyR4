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
├── sensors/              # Scripts for sensor data (real or simulated)
│   └── sensor_ingest.py  # First script: generate or simulate sensor readings
│
├── api_wrappers/         # External API modules
│   └── openweather.py    # First wrapper: fetch weather data
│   └── nasa_power.py     # Second wrapper: fetch solar/irradiance data
│
├── db/                   # Database setup and connectors
│   └── schema.sql        # SQL commands to create tables
│   └── db_connector.py   # Python script to insert/read data
│
├── preprocessing/        # Data cleaning scripts
│   └── preprocess.py     # First script: normalize and clean sensor logs
│
├── notebooks/            # Jupyter notebooks for demos
│   └── data_pipeline_demo.ipynb  # Step-by-step interactive demo
│
├── requirements.txt      # List of Python dependencies
└── README.md             # Documentation for setup and usage

## my notes
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