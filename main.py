import logging

from api.woocommerce import fetch_and_process_sales_data
from config.logs import setup_logging

setup_logging()  # Set up logging configurations


def ingest_woocommerce_data_job():
  logging.info("Fetching sales data...")
  sales_data = fetch_and_process_sales_data()
  if sales_data is not None:
    logging.info("Fetched sales data successfully.")
  else:
    logging.error("Failed to fetch sales data.")


def main():
  ingest_woocommerce_data_job()


if __name__ == "__main__":
  main()
