
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

url = "https://books.toscrape.com/"

try:
    response = requests.get(url, timeout=15)
    response.raise_for_status()

    print("Website status:", response.status_code)

    soup = BeautifulSoup(response.text, "html.parser")
    links = soup.find_all("a", href=True)

    print("Total links found:", len(links))

    for link in links:
        text = link.get_text(" ", strip=True)
        full_url = urljoin(url, link["href"])

        print(f"Text: {text} | URL: {full_url}")

except requests.RequestException as error:
    print("Request error:", error)
