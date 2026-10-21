
import requests
from bs4 import BeautifulSoup

url = "https://books.toscrape.com/"
headers = {
    "User-Agent": "Mozilla/5.0 (compatible; LearningScraper/1.0)"
}

try:
    response = requests.get(
        url,
        headers=headers,
        timeout=20
    )
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    print("=" * 50)
    print("DAY 3 - WEB SCRAPING: EXTRACT HEADINGS")
    print("=" * 50)
    print("Website:", url)
    print("HTTP Status:", response.status_code)

    found = False

    for tag in ["h1", "h2", "h3"]:
        headings = soup.find_all(tag)
        print(f"\nTotal {tag} headings: {len(headings)}")

        for heading in headings:
            text = heading.get_text(" ", strip=True)
            print(f"{tag.upper()}: {text}")
            found = True

    if not found:
        print("\nNo H1, H2, or H3 headings found.")
        print("Check the downloaded HTML or try another permitted page.")

except requests.RequestException as error:
    print("Unable to fetch the webpage.")
    print("Error:", error)

print("=" * 50)
