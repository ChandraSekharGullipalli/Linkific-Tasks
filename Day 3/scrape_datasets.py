
import csv
import time
from pathlib import Path

import requests
from bs4 import BeautifulSoup

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

HEADERS = {
    "User-Agent": "LinkificTrainingScraper/1.0"
}

SOURCES = [
    {
        "name": "books_main",
        "url": "https://books.toscrape.com/",
        "output": "books_main.csv",
    },
    {
        "name": "books_fiction",
        "url": "https://books.toscrape.com/catalogue/category/books/fiction_10/index.html",
        "output": "books_fiction.csv",
    },
    {
        "name": "books_travel",
        "url": "https://books.toscrape.com/catalogue/category/books/travel_2/index.html",
        "output": "books_travel.csv",
    },
]


def scrape_books(url):
    response = requests.get(
        url, headers=HEADERS, timeout=20
    )
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    records = []

    for book in soup.select("article.product_pod"):
        title_tag = book.select_one("h3 a")
        price_tag = book.select_one(".price_color")
        availability_tag = book.select_one(
            ".availability"
        )

        records.append({
            "title": (
                title_tag.get("title", "").strip()
                if title_tag else ""
            ),
            "price": (
                price_tag.get_text(strip=True)
                if price_tag else ""
            ),
            "availability": (
                availability_tag.get_text(" ", strip=True)
                if availability_tag else ""
            ),
            "source_url": url,
        })

    return records


def save_csv(records, filepath):
    fields = [
        "title", "price", "availability", "source_url"
    ]

    with open(
        filepath, "w", newline="", encoding="utf-8-sig"
    ) as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(records)


def main():
    summary = []

    for source in SOURCES:
        print(f"\nScraping: {source['name']}")

        try:
            records = scrape_books(source["url"])

            output_path = DATA_DIR / source["output"]
            save_csv(records, output_path)

            print("Records collected:", len(records))
            print("Saved to:", output_path)

            summary.append({
                "source": source["name"],
                "url": source["url"],
                "records": len(records),
                "status": "Success",
            })

        except (requests.RequestException, OSError) as error:
            print("Error:", error)

            summary.append({
                "source": source["name"],
                "url": source["url"],
                "records": 0,
                "status": f"Failed: {error}",
            })

        time.sleep(1)

    summary_path = DATA_DIR / "scraping_summary.csv"
    save_summary(summary, summary_path)

    print("\nScraping completed.")
    print("Summary saved to:", summary_path)


def save_summary(records, filepath):
    fields = ["source", "url", "records", "status"]

    with open(
        filepath, "w", newline="", encoding="utf-8-sig"
    ) as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(records)


if __name__ == "__main__":
    main()
