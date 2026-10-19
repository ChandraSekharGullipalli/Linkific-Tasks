
import requests

url = "https://api.open-meteo.com/v1/forecast"

params = {
    "latitude": 17.385,
    "longitude": 78.4867,
    "current": "temperature_2m,relative_humidity_2m"
}

try:
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()

    data = response.json()

    print("Weather API Integration")
    print("Temperature:", data["current"]["temperature_2m"], "°C")
    print("Humidity:", data["current"]["relative_humidity_2m"], "%")

except requests.RequestException as error:
    print("API request failed:", error)
