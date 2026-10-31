
from pathlib import Path
import json
import logging

import pandas as pd
import requests

# Get folders based on this Python file's location
BASE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BASE_DIR.parent

DATA_DIR = PROJECT_DIR / "Data"
OUTPUT_DIR = PROJECT_DIR / "output"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Configure logging
logging.basicConfig(
    filename=str(OUTPUT_DIR / "error_handling.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def handle_csv():
    try:
        file_path = DATA_DIR / "hospital_patients.csv"
        data = pd.read_csv(file_path)

        if data.empty:
            raise ValueError("CSV file is empty")

        print(f"CSV extraction successful: {len(data)} records")
        logging.info("CSV extraction successful")

    except FileNotFoundError:
        print("Error: CSV file not found")
        logging.exception("CSV file not found")

    except (pd.errors.ParserError, pd.errors.EmptyDataError, ValueError):
        print("Error: CSV file is invalid or empty")
        logging.exception("CSV processing error")


def handle_api():
    try:
        url = "https://jsonplaceholder.typicode.com/posts"
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()

        if not isinstance(data, list):
            raise ValueError("Unexpected API response format")

        print(f"API extraction successful: {len(data)} records")
        logging.info("API extraction successful")

    except requests.exceptions.RequestException:
        print("Error: API request failed")
        logging.exception("API request failed")

    except ValueError:
        print("Error: Invalid API response")
        logging.exception("Invalid API response")


def handle_json():
    try:
        file_path = DATA_DIR / "online_courses.json"

        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, list):
            raise ValueError("JSON data must be a list")

        print(f"JSON extraction successful: {len(data)} records")
        logging.info("JSON extraction successful")

    except FileNotFoundError:
        print("Error: JSON file not found")
        logging.exception("JSON file not found")

    except json.JSONDecodeError:
        print("Error: JSON file contains invalid data")
        logging.exception("Invalid JSON format")

    except ValueError:
        print("Error: Unexpected JSON data format")
        logging.exception("JSON data format error")


if __name__ == "__main__":
    print("ERROR HANDLING STARTED")

    handle_csv()
    handle_api()
    handle_json()

    print("ERROR HANDLING COMPLETED")
