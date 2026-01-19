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

