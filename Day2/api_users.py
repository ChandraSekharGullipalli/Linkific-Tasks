
import requests

url = "https://jsonplaceholder.typicode.com/users"

try:
    response = requests.get(url, timeout=10)
    response.raise_for_status()

    users = response.json()

    print("Users API Integration")
    print("=" * 30)

    for user in users[:5]:
        print("Name:", user["name"])
        print("Email:", user["email"])
        print("City:", user["address"]["city"])
        print("-" * 30)

except requests.RequestException as error:
    print("API request failed:", error)
