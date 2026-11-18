
"""
Day 23 - Web Scraping
Website: Books to Scrape

Features:
- Multi-page scraping
- Product title extraction
- Price extraction
- Availability extraction
- Product URL extraction
- Error handling
- Logging
- Raw JSON storage
"""

import json
import logging
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


# --------------------------------------------------
# 1. PROJECT CONFIGURATION
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[3]

RAW_DIR = PROJECT_ROOT / "data" / "raw" / "scraped"
LOG_DIR = PROJECT_ROOT / "logs"

RAW_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)

BASE_URL = "https://books.toscrape.com/"


# --------------------------------------------------
# 2. LOGGING CONFIGURATION
# --------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(
            LOG_DIR / "web_scraping.log",
            encoding="utf-8"
        ),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


# --------------------------------------------------
# 3. HTTP SESSION
# --------------------------------------------------

def create_session():

    session = requests.Session()

    session.headers.update({
        "User-Agent": (
            "Mozilla/5.0 "
            "(Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 Chrome/120.0 Safari/537.36"
        )
    })

    return session


# --------------------------------------------------
# 4. FETCH WEBSITE PAGE
# --------------------------------------------------

def fetch_page(session, url):

    try:

        response = session.get(
            url,
            timeout=30
        )

        response.raise_for_status()

        logger.info("Successfully fetched: %s", url)

        return response.text

    except requests.RequestException as error:

        logger.error(
            "Failed to fetch %s: %s",
            url,
            error
        )

        return None


# --------------------------------------------------
# 5. EXTRACT PRODUCT INFORMATION
# --------------------------------------------------

def extract_products(html, page_url):

    soup = BeautifulSoup(html, "html.parser")

    products = []

    product_elements = soup.select("article.product_pod")

    for product in product_elements:

        try:

            title_element = product.select_one("h3 a")
            price_element = product.select_one(
                "p.price_color"
            )
            availability_element = product.select_one(
                "p.instock.availability"
            )

            if not title_element:
                logger.warning("Product title missing")
                continue

            title = title_element.get("title")

            product_url = urljoin(
                page_url,
                title_element.get("href")
            )

            price = (
                price_element.get_text(strip=True)
                if price_element
                else None
            )

            availability = (
                availability_element.get_text(strip=True)
                if availability_element
                else "Unknown"
            )

            rating_element = product.select_one(
                "p.star-rating"
            )

            rating = (
                rating_element.get("class", [])[-1]
                if rating_element
                and len(rating_element.get("class", [])) > 1
                else None
            )

            products.append({
                "product_title": title,
                "price": price,
                "availability": availability,
                "rating": rating,
                "product_url": product_url
            })

        except Exception as error:

            logger.error(
                "Product extraction error: %s",
                error
            )

    return products


# --------------------------------------------------
# 6. SAVE RAW SCRAPED DATA
# --------------------------------------------------

def save_data(records):

    timestamp = datetime.now(
        timezone.utc
    ).strftime("%Y%m%d_%H%M%S")

    output_file = (
        RAW_DIR /
        f"scraped_products_{timestamp}.json"
    )

    output = {
        "source": "Books to Scrape",
        "source_url": BASE_URL,
        "collected_at": datetime.now(
            timezone.utc
        ).isoformat(),
        "record_count": len(records),
        "records": records
    }

    with output_file.open(
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            output,
            file,
            indent=4,
            ensure_ascii=False
        )

    logger.info(
        "Saved %s products to %s",
        len(records),
        output_file
    )


# --------------------------------------------------
# 7. MAIN SCRAPING PIPELINE
# --------------------------------------------------

def main():

    logger.info("=" * 60)
    logger.info("DAY 23 WEB SCRAPING STARTED")
    logger.info("=" * 60)

    session = create_session()

    all_products = []

    try:

        # Scrape first three pages
        for page_number in range(1, 4):

            if page_number == 1:
                page_url = BASE_URL
            else:
                page_url = urljoin(
                    BASE_URL,
                    f"catalogue/page-{page_number}.html"
                )

            logger.info(
                "Scraping page %s",
                page_number
            )

            html = fetch_page(
                session,
                page_url
            )

            if html is None:
                logger.warning(
                    "Skipping page %s",
                    page_number
                )
                continue

            products = extract_products(
                html,
                page_url
            )

            logger.info(
                "Page %s: %s products extracted",
                page_number,
                len(products)
            )

            all_products.extend(products)

            # Be respectful to the website
            time.sleep(1)

    finally:

        session.close()

    if all_products:

        save_data(all_products)

    else:

        logger.warning(
            "No products collected. Check website connectivity."
        )

    logger.info(
        "Total products collected: %s",
        len(all_products)
    )

    logger.info("=" * 60)
    logger.info("WEB SCRAPING COMPLETED")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
