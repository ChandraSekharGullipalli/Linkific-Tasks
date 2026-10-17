
import json
import urllib.request

# API URL
url = "https://jsonplaceholder.typicode.com/users"

# Send a request to the API
with urllib.request.urlopen(url) as response:
    data = json.loads(response.read().decode("utf-8"))

# Parse and display the JSON response
print("User Details")
print("-" * 40)

for user in data:
    print("ID:", user["id"])
    print("Name:", user["name"])
    print("Email:", user["email"])
    print("City:", user["address"]["city"])
    print("-" * 40)
