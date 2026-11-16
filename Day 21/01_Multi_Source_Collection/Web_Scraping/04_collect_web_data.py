
"""
Day 21 - Web Scraping Data Collection
Collects quotes from a practice website using Requests and BeautifulSoup.
Saves the collected information as CSV and JSON.
"""

import json
import logging
from pathlib import Path

import pandas as pd
import requests
from bs4 import BeautifulSoup

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "output" / "Web_Scraping"
LOG_DIR = BASE_DIR / "logs"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(
            LOG_DIR / "web_scraping.log",
            encoding="utf-8"
        ),
        logging.StreamHandler()
    ],
    force=True
)

logger = logging.getLogger(__name__)

URL = "https://quotes.toscrape.com/"


def collect_quotes():
    try:
        logger.info("Starting web scraping")
        logger.info("Website: %s", URL)

        response = requests.get(
            URL,
            timeout=30,
            headers={"User-Agent": "Mozilla/5.0"}
        )
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        quotes = []

        for item in soup.select(".quote"):
            quote_text = item.select_one(".text")
            author = item.select_one(".author")
            tags = item.select(".tags .tag")

            quotes.append({
                "quote": quote_text.get_text(strip=True),
                "author": author.get_text(strip=True),
                "tags": ", ".join(
                    tag.get_text(strip=True) for tag in tags
                )
            })

        if not quotes:
            logger.warning("No quotes were found")
            return

        dataframe = pd.DataFrame(quotes)

        csv_path = OUTPUT_DIR / "scraped_quotes.csv"
        json_path = OUTPUT_DIR / "scraped_quotes.json"

        dataframe.to_csv(csv_path, index=False)

        with open(json_path, "w", encoding="utf-8") as file:
            json.dump(
                quotes,
                file,
                indent=4,
                ensure_ascii=False
            )

        logger.info("Records collected: %s", len(quotes))
        logger.info("CSV saved: %s", csv_path)
        logger.info("JSON saved: %s", json_path)
        logger.info("Web scraping completed successfully")

    except requests.RequestException:
        logger.exception("Website request failed")
    except Exception:
        logger.exception("Web scraping failed")


if __name__ == "__main__":
    collect_quotes()
