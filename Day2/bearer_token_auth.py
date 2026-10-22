
import requests
import os

# Public demo API endpoint
url = "https://httpbin.org/bearer"

# Read the token from an environment variable
token = os.getenv("API_BEARER_TOKEN")

if not token:
    print("Token not found. Set API_BEARER_TOKEN first.")
else:
    headers = {
        "Authorization": f"Bearer {token}"
    }

    try:
        response = requests.get(
            url,
            headers=headers,
            timeout=10
        )

        if response.status_code == 200:
            print("Bearer Token Authentication Successful")
            print(response.json())
        elif response.status_code == 401:
            print("Authentication failed. Check your token.")
        else:
            print("Request failed:", response.status_code)

    except requests.RequestException as error:
        print("API request error:", error)
