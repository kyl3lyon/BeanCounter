import logging

from api.woocommerce import fetch_and_process_sales_data
from config.logs import setup_logging

setup_logging()  # Set up logging configurations


def main():
  # Log start of fetching process
  logging.info("Fetching sales data...")
  sales_data = fetch_and_process_sales_data()
  if sales_data is not None:
    # Log successful fetch and processing
    logging.info("Fetched sales data successfully.")
  else:
    # Log error message
    logging.error("Failed to fetch sales data.")


if __name__ == "__main__":
  main()
