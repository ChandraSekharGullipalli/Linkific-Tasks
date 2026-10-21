
import requests
from bs4 import BeautifulSoup

url = "https://example.com"

try:
    response = requests.get(
        url,
        timeout=15,
        headers={"User-Agent": "LearningScraper/1.0"}
    )
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    if soup.title:
        print("Page title:", soup.title.get_text(strip=True))
    else:
        print("No title found.")

except requests.RequestException as error:
    print("Error fetching webpage:", error)
