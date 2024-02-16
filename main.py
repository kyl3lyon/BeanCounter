import logging

from api.woocommerce import fetch_and_process_sales_data
from config.logs import setup_logging


def ingest_woocommerce_data_job():
  logging.info("Fetching sales data...")
  sales_data = fetch_and_process_sales_data()
  if sales_data:  # If there's some data, log success.
    logging.info("Fetched sales data successfully.")


# def start_dash_app():
# dash_app.run_server(debug=True)


def main():
  ingest_woocommerce_data_job()  # Fetch and process sales data
  # start_dash_app()  # Start the Dash app


if __name__ == "__main__":
  setup_logging()  # Set up logging configurations
  main()
