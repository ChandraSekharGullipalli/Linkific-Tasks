
import requests

url = "https://jsonplaceholder.typicode.com/posts"

try:
    response = requests.get(url, timeout=10)
    response.raise_for_status()

    posts = response.json()

    print("Posts API Integration")
    print("=" * 40)

    for post in posts[:5]:
        print("Post ID:", post["id"])
        print("Title:", post["title"])
        print("Body:", post["body"])
        print("-" * 40)

except requests.RequestException as error:
    print("API request failed:", error)
