
import requests
import csv
from pathlib import Path

url = "https://jsonplaceholder.typicode.com/posts"

try:
    response = requests.get(url, timeout=15)
    response.raise_for_status()

    posts = response.json()

    if not posts:
        print("No data received from the API.")
    else:
        output_file = Path(__file__).parent / "api_posts_dataset.csv"

        fieldnames = ["userId", "id", "title", "body"]

        with output_file.open(
            "w", newline="", encoding="utf-8"
        ) as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(posts)

        print("Dataset collected successfully!")
        print("Total records:", len(posts))
        print("Saved to:", output_file)

except requests.RequestException as error:
    print("API request failed:", error)

except (OSError, csv.Error) as error:
    print("File error:", error)
