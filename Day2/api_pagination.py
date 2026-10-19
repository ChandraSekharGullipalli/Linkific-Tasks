
import requests

url = "https://jsonplaceholder.typicode.com/posts"

page = 1
limit = 10

try:
    while True:
        params = {
            "_page": page,
            "_limit": limit
        }

        response = requests.get(
            url,
            params=params,
            timeout=10
        )
        response.raise_for_status()

        posts = response.json()

        if not posts:
            print("No more posts available.")
            break

        print(f"\nPage {page}")
        print("-" * 40)

        for post in posts:
            print("ID:", post["id"])
            print("Title:", post["title"])

        page += 1

except requests.RequestException as error:
    print("API request failed:", error)
