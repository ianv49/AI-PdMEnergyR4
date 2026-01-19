import requests
from datetime import datetime

API_KEY = "0723d71a05e58ae3f7fc91e39a901e6b"
CITY = "Manila"  # change to your location
URL = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"

def get_weather_data():
    """Fetch wind + solar data from OpenWeather API."""
    response = requests.get(URL)
    data = response.json()

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    wind_speed = data["wind"]["speed"]
    wind_dir = data["wind"]["deg"]

    # Approximate solar irradiance using cloud cover
    cloudiness = data["clouds"]["all"]  # %
    solar_irradiance = round((100 - cloudiness) * 10)  # W/m² approx

    return (timestamp, wind_speed, wind_dir, solar_irradiance)

