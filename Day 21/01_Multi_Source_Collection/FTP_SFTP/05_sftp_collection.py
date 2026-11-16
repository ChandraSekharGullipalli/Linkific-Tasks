
"""
Day 21 - SFTP Data Collection
Automated file transfer using Paramiko.
"""

import logging
from pathlib import Path

import pandas as pd
import paramiko


# --------------------------------------------------
# 1. PROJECT PATHS AND SFTP CONFIGURATION
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

LOCAL_FILE = BASE_DIR / "FTP_SFTP" / "local_server" / "employees.csv"

DOWNLOAD_DIR = BASE_DIR / "output" / "FTP_SFTP"
DOWNLOAD_FILE = DOWNLOAD_DIR / "employees_downloaded_paramiko.csv"
JSON_FILE = DOWNLOAD_DIR / "employees_downloaded.json"

LOG_DIR = BASE_DIR / "logs"
LOG_FILE = LOG_DIR / "sftp_collection.log"

HOST = "localhost"
PORT = 22
USERNAME = "chandra sekhar"

# Private key stays on your computer. Never upload it to GitHub.
KEY_PATH = Path.home() / ".ssh" / "day21_sftp_key"

REMOTE_DIR = "sftp_practice"
REMOTE_FILENAME = "employees.csv"


# --------------------------------------------------
# 2. CREATE REQUIRED DIRECTORIES
# --------------------------------------------------

DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------
# 3. CONFIGURE LOGGING
# --------------------------------------------------

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)


# --------------------------------------------------
# 4. SFTP COLLECTION FUNCTION
# --------------------------------------------------

def collect_sftp_data():

    transport = None
    sftp = None

    try:
        print("Starting SFTP collection...")

        # Check local input file and SSH key
        if not LOCAL_FILE.exists():
            raise FileNotFoundError(f"Local CSV not found: {LOCAL_FILE}")

        if not KEY_PATH.exists():
            raise FileNotFoundError(f"SSH private key not found: {KEY_PATH}")

        # Load the ED25519 private key
        private_key = paramiko.Ed25519Key.from_private_key_file(
            str(KEY_PATH)
        )

        # Establish SSH transport
        transport = paramiko.Transport((HOST, PORT))

        transport.connect(
            username=USERNAME,
            pkey=private_key
        )

        # Create SFTP client
        sftp = paramiko.SFTPClient.from_transport(transport)

        print("SFTP connection successful!")
        logging.info("Connected to SFTP server.")

        # Move into the remote practice directory
        sftp.chdir(REMOTE_DIR)

        # Upload the CSV file
        sftp.put(str(LOCAL_FILE), REMOTE_FILENAME)

        print("CSV uploaded successfully.")
        logging.info("Uploaded file: %s", REMOTE_FILENAME)

        # List files available on the remote server
        remote_files = sftp.listdir()

        print("\nRemote files:")
        for filename in remote_files:
            print("-", filename)

        # Download the CSV file
        sftp.get(
            REMOTE_FILENAME,
            str(DOWNLOAD_FILE)
        )

        print("\nCSV downloaded successfully.")
        logging.info("Downloaded file: %s", DOWNLOAD_FILE.name)

        # Read and validate downloaded CSV
        dataframe = pd.read_csv(DOWNLOAD_FILE)

        print("\nDownloaded records:")
        print(dataframe)

        print(f"\nTotal records collected: {len(dataframe)}")

        # Check required columns
        required_columns = [
            "employee_id",
            "employee_name",
            "department",
            "salary"
        ]

        if not all(column in dataframe.columns for column in required_columns):
            raise ValueError("Downloaded CSV is missing required columns.")

        if dataframe.empty:
            raise ValueError("Downloaded CSV contains no records.")

        # Save JSON copy
        dataframe.to_json(
            JSON_FILE,
            orient="records",
            indent=4
        )

        print("\nJSON file created:", JSON_FILE.name)

        logging.info(
            "Validation successful. Total records: %s",
            len(dataframe)
        )

        print("\nSFTP collection completed successfully!")

    except Exception as error:
        logging.exception("SFTP collection failed.")
        print("\nSFTP collection failed:", error)

    finally:
        if sftp is not None:
            sftp.close()

        if transport is not None:
            transport.close()

        print("\nSFTP connection closed.")


# --------------------------------------------------
# 5. RUN THE COLLECTION
# --------------------------------------------------

if __name__ == "__main__":
    collect_sftp_data()

