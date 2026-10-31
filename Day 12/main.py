
import logging
import os

from extract import extract_sales, extract_customers
from transform import transform_data
from load import load_data

# Create logs folder
os.makedirs("logs", exist_ok=True)
os.makedirs("output", exist_ok=True)

# Configure logging
logging.basicConfig(
    filename="logs/etl_pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def run_etl_pipeline():

    try:
        print("\n========== ETL PIPELINE STARTED ==========")
        logging.info("ETL pipeline started")

        # 1. Extract
        sales = extract_sales()
        customers = extract_customers()

        # 2. Transform
        transformed_data = transform_data(sales, customers)

        # Save transformed data as CSV
        transformed_data.to_csv(
            "output/cleaned_sales.csv",
            index=False
        )

        print("\nTransformed CSV saved successfully!")

        # 3. Load
        load_data(transformed_data)

        print("\n========== ETL PIPELINE COMPLETED ==========")
        logging.info("ETL pipeline completed successfully")

    except Exception:
        logging.exception("ETL pipeline failed")
        print("\nETL pipeline failed. Check logs/etl_pipeline.log")
        raise

if __name__ == "__main__":
    run_etl_pipeline()
