import logging

from api.woocommerce import fetch_and_process_sales_data
from config.logs import setup_logging

setup_logging()  # Set up logging configurations


def ingest_woocommerce_data_job():
  logging.info("Fetching sales data...")
  sales_data = fetch_and_process_sales_data()
  if sales_data:  # If there's some data, log success.
    logging.info("Fetched sales data successfully.")


def main():
  ingest_woocommerce_data_job()


if __name__ == "__main__":
  main()
