
import requests

url = "https://api.openweathermap.org/data/2.5/weather"

api_key = "YOUR_API_KEY"

params = {
    "q": "Hyderabad",
    "appid": api_key
}

try:
    response = requests.get(url, params=params, timeout=10)

    if response.status_code == 200:
        data = response.json()
        print("API Key Authentication Successful")
        print("City:", data["name"])
        print("Weather:", data["weather"][0]["description"])

    elif response.status_code == 401:
        print("Authentication failed. Check your API key.")

    else:
        print("Request failed:", response.status_code)

except requests.RequestException as error:
    print("API request error:", error)
