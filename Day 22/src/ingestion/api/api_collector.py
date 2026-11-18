
"""
Day 23 - API Data Collection
Sources:
1. GitHub REST API
2. JSONPlaceholder API
3. Open Library API

Features:
- Pagination
- Optional GitHub authentication
- Retry handling
- Rate-limit handling
- Error handling
- Logging
- Raw JSON storage
"""

import json
import logging
import os
import time
from datetime import datetime, timezone
from pathlib import Path

import requests
from dotenv import load_dotenv
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


# --------------------------------------------------
# 1. PROJECT CONFIGURATION
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[3]
RAW_API_DIR = PROJECT_ROOT / "data" / "raw" / "api"
LOG_DIR = PROJECT_ROOT / "logs"

RAW_API_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)

load_dotenv(PROJECT_ROOT / ".env")

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")


# --------------------------------------------------
# 2. LOGGING CONFIGURATION
# --------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(
            LOG_DIR / "api_collection.log",
            encoding="utf-8"
        ),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


# --------------------------------------------------
# 3. CREATE HTTP SESSION WITH RETRIES
# --------------------------------------------------

def create_session():
    """Create a reusable HTTP session with retry support."""

    retry_strategy = Retry(
        total=4,
        connect=4,
        read=4,
        status=4,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"],
        respect_retry_after_header=True,
    )

    adapter = HTTPAdapter(max_retries=retry_strategy)

    session = requests.Session()
    session.mount("https://", adapter)
    session.mount("http://", adapter)

    session.headers.update({
        "User-Agent": "Linkific-Data-Engineering-Project/1.0"
    })

    return session


# --------------------------------------------------
# 4. SAVE RAW API DATA
# --------------------------------------------------

def save_raw_data(source, records):
    """Save collected records as timestamped JSON."""

    timestamp = datetime.now(timezone.utc).strftime(
        "%Y%m%d_%H%M%S"
    )

    output_file = RAW_API_DIR / f"{source}_{timestamp}.json"

    payload = {
        "source": source,
        "collected_at": datetime.now(timezone.utc).isoformat(),
        "record_count": len(records),
        "records": records
    }

    with output_file.open("w", encoding="utf-8") as file:
        json.dump(payload, file, indent=4, ensure_ascii=False)

    logger.info(
        "%s: saved %s records to %s",
        source,
        len(records),
        output_file
    )

    return output_file


# --------------------------------------------------
# 5. COMMON API REQUEST
# --------------------------------------------------

def get_json(session, url, params=None):
    """Send GET request and return JSON response."""

    response = session.get(
        url,
        params=params,
        timeout=30
    )

    # Respect an API-provided rate-limit wait time
    if response.status_code == 403 and response.headers.get(
        "X-RateLimit-Remaining"
    ) == "0":
        reset_time = response.headers.get("X-RateLimit-Reset")

        if reset_time:
            wait_seconds = max(
                0,
                int(reset_time) - int(time.time())
            )

            logger.warning(
                "API rate limit reached. Waiting %s seconds.",
                wait_seconds
            )

            time.sleep(min(wait_seconds, 60))

            response = session.get(
                url,
                params=params,
                timeout=30
            )

    response.raise_for_status()
    return response.json()


# --------------------------------------------------
# 6. GITHUB API COLLECTION
# --------------------------------------------------

def collect_github(session):
    """
    Collect public repositories from GitHub.
    Uses page-based pagination.
    """

    logger.info("Starting GitHub collection")

    url = "https://api.github.com/search/repositories"

    headers = {}

    if GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"
        logger.info("GitHub authentication enabled")
    else:
        logger.info("Using GitHub unauthenticated access")

    records = []

    for page in range(1, 4):

        params = {
            "q": "data engineering",
            "sort": "stars",
            "order": "desc",
            "per_page": 10,
            "page": page
        }

        try:
            response = session.get(
                url,
                params=params,
                headers=headers,
                timeout=30
            )

            response.raise_for_status()
            data = response.json()

            items = data.get("items", [])

            if not items:
                break

            for item in items:
                records.append({
                    "repository_id": item.get("id"),
                    "name": item.get("name"),
                    "full_name": item.get("full_name"),
                    "description": item.get("description"),
                    "stars": item.get("stargazers_count"),
                    "language": item.get("language"),
                    "html_url": item.get("html_url")
                })

            logger.info(
                "GitHub page %s collected: %s records",
                page,
                len(items)
            )

        except requests.RequestException as error:
            logger.error("GitHub page %s failed: %s", page, error)
            break

    if records:
        save_raw_data("github_repositories", records)

    logger.info("GitHub total records: %s", len(records))


# --------------------------------------------------
# 7. JSONPLACEHOLDER API COLLECTION
# --------------------------------------------------

def collect_jsonplaceholder(session):
    """
    Collect posts from JSONPlaceholder.
    Uses _page and _limit pagination.
    """

    logger.info("Starting JSONPlaceholder collection")

    url = "https://jsonplaceholder.typicode.com/posts"

    records = []

    for page in range(1, 4):

        params = {
            "_page": page,
            "_limit": 20
        }

        try:
            data = get_json(session, url, params)

            if not data:
                break

            for item in data:
                records.append({
                    "post_id": item.get("id"),
                    "user_id": item.get("userId"),
                    "title": item.get("title"),
                    "body": item.get("body")
                })

            logger.info(
                "JSONPlaceholder page %s collected: %s records",
                page,
                len(data)
            )

        except requests.RequestException as error:
            logger.error(
                "JSONPlaceholder page %s failed: %s",
                page,
                error
            )
            break

    if records:
        save_raw_data("jsonplaceholder_posts", records)

    logger.info("JSONPlaceholder total records: %s", len(records))


# --------------------------------------------------
# 8. OPEN LIBRARY API COLLECTION
# --------------------------------------------------

def collect_open_library(session):
    """
    Collect book search results from Open Library.
    Uses offset-based pagination.
    """

    logger.info("Starting Open Library collection")

    url = "https://openlibrary.org/search.json"

    records = []

    for page in range(3):

        params = {
            "q": "data engineering",
            "limit": 10,
            "offset": page * 10
        }

        try:
            data = get_json(session, url, params)

            books = data.get("docs", [])

            if not books:
                break

            for book in books:
                records.append({
                    "title": book.get("title"),
                    "author": book.get("author_name", []),
                    "first_publish_year": book.get(
                        "first_publish_year"
                    ),
                    "isbn": book.get("isbn", [])[:3],
                    "edition_count": book.get("edition_count"),
                    "open_library_key": book.get("key")
                })

            logger.info(
                "Open Library page %s collected: %s records",
                page + 1,
                len(books)
            )

        except requests.RequestException as error:
            logger.error(
                "Open Library page %s failed: %s",
                page + 1,
                error
            )
            break

    if records:
        save_raw_data("open_library_books", records)

    logger.info("Open Library total records: %s", len(records))


# --------------------------------------------------
# 9. MAIN EXECUTION
# --------------------------------------------------

def main():

    logger.info("=" * 60)
    logger.info("DAY 23 API DATA COLLECTION STARTED")
    logger.info("=" * 60)

    session = create_session()

    try:
        collect_github(session)
        collect_jsonplaceholder(session)
        collect_open_library(session)

    finally:
        session.close()

    logger.info("=" * 60)
    logger.info("API DATA COLLECTION COMPLETED")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
