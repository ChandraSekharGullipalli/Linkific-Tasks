
"""
Day 21 - Multi-Source Data Collection
Task: Collect data from three different REST APIs.

APIs:
1. JSONPlaceholder - User data
2. DummyJSON - Product data
3. Open-Meteo - Weather data

Outputs:
- JSON files
- CSV files
- Execution log
"""

import json
import logging
from pathlib import Path
from datetime import datetime, timezone

import requests
import pandas as pd


# --------------------------------------------------
# 1. PROJECT PATHS
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

OUTPUT_DIR = BASE_DIR / "output" / "APIs"
LOG_DIR = BASE_DIR / "logs"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------
# 2. LOGGING CONFIGURATION
# --------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "api_collection.log", encoding="utf-8"),
        logging.StreamHandler()
    ],
    force=True
)

logger = logging.getLogger(__name__)


# --------------------------------------------------
# 3. COMMON API COLLECTION FUNCTION
# --------------------------------------------------

def fetch_api_data(url, params=None):
    """
    Connect to an API and return JSON data.
    Handles connection and HTTP errors.
    """

    try:
        logger.info(f"Connecting to API: {url}")

        response = requests.get(
            url,
            params=params,
            timeout=30
        )

        response.raise_for_status()

        data = response.json()

        logger.info("API data collected successfully.")

        return data

    except requests.exceptions.Timeout:
        logger.error(f"API request timed out: {url}")

    except requests.exceptions.HTTPError as error:
        logger.error(f"HTTP error: {error}")

    except requests.exceptions.ConnectionError:
        logger.error(f"Connection error: {url}")

    except requests.exceptions.RequestException as error:
        logger.error(f"Request failed: {error}")

    except ValueError as error:
        logger.error(f"Invalid JSON response: {error}")

    return None


# --------------------------------------------------
# 4. SAVE DATA INTO JSON AND CSV
# --------------------------------------------------

def save_data(data, filename):
    """
    Save collected records into JSON and CSV formats.
    """

    if not data:
        logger.warning(f"No data available for {filename}")
        return

    json_path = OUTPUT_DIR / f"{filename}.json"
    csv_path = OUTPUT_DIR / f"{filename}.csv"

    try:
        # Save raw JSON data
        with open(json_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

        # Convert records into DataFrame
        dataframe = pd.json_normalize(data)

        # Save CSV file
        dataframe.to_csv(csv_path, index=False)

        logger.info(f"JSON saved: {json_path}")
        logger.info(f"CSV saved: {csv_path}")
        logger.info(f"Total records: {len(dataframe)}")

    except (OSError, TypeError, ValueError) as error:
        logger.exception(f"Error saving {filename}: {error}")


# --------------------------------------------------
# 5. API 1 - JSONPLACEHOLDER
# --------------------------------------------------

def collect_users():

    logger.info("Starting API 1: JSONPlaceholder")

    url = "https://jsonplaceholder.typicode.com/users"

    data = fetch_api_data(url)

    if data is not None:
        save_data(data, "users")
    else:
        logger.warning("User collection failed.")


# --------------------------------------------------
# 6. API 2 - DUMMYJSON
# --------------------------------------------------

def collect_products():

    logger.info("Starting API 2: DummyJSON")

    url = "https://dummyjson.com/products"

    params = {
        "limit": 30
    }

    response_data = fetch_api_data(url, params)

    if response_data is not None:
        products = response_data.get("products", [])

        save_data(products, "products")
    else:
        logger.warning("Product collection failed.")


# --------------------------------------------------
# 7. API 3 - OPEN-METEO
# --------------------------------------------------

def collect_weather():

    logger.info("Starting API 3: Open-Meteo")

    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": 51.5074,
        "longitude": -0.1278,
        "current": "temperature_2m,relative_humidity_2m,wind_speed_10m",
        "timezone": "auto"
    }

    response_data = fetch_api_data(url, params)

    if response_data is not None:

        weather_record = {
            "latitude": response_data.get("latitude"),
            "longitude": response_data.get("longitude"),
            "timezone": response_data.get("timezone"),
            "collection_time_utc": datetime.now(timezone.utc).isoformat(),
            "current": response_data.get("current", {})
        }

        save_data([weather_record], "weather")

    else:
        logger.warning("Weather collection failed.")


# --------------------------------------------------
# 8. MAIN EXECUTION
# --------------------------------------------------

def main():

    logger.info("=" * 60)
    logger.info("MULTI-SOURCE API DATA COLLECTION STARTED")
    logger.info("=" * 60)

    collect_users()

    collect_products()

    collect_weather()

    logger.info("=" * 60)
    logger.info("API DATA COLLECTION COMPLETED")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
