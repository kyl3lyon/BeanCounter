import logging

import pandas as pd
from woocommerce import API

from config.logs import setup_logging
from config.settings import (
    WOO_COMMERCE_CONSUMER_KEY,
    WOO_COMMERCE_CONSUMER_SECRET,
    WOO_COMMERCE_URL,
)
from database.db import get_last_processed_timestamp, insert_sales_data_to_db

setup_logging()  # Set up logging configurations


def get_wc_api():
  return API(url=WOO_COMMERCE_URL,
             consumer_key=WOO_COMMERCE_CONSUMER_KEY,
             consumer_secret=WOO_COMMERCE_CONSUMER_SECRET,
             version="wc/v3")


def process_sales_data(data):
  # Convert the list of dictionaries to a DataFrame
  df = pd.DataFrame(data)

  # Normalize 'billing' and 'shipping' fields
  billing_df = pd.json_normalize(df['billing'])
  shipping_df = pd.json_normalize(df['shipping'])

  # Directly extract 'href' values from '_links' field
  df['LINK_SELF'] = df['_links'].apply(lambda x: x['self'][0]['href']
                                       if 'self' in x else None)
  df['LINK_COLLECTION'] = df['_links'].apply(
      lambda x: x['collection'][0]['href'] if 'collection' in x else None)

  # Concatenate the normalized billing and shipping dataframes with the original df
  df = pd.concat([
      df.drop(columns=['billing', 'shipping', '_links']),
      billing_df.add_prefix('BILLING_'),
      shipping_df.add_prefix('SHIPPING_')
  ],
                 axis=1)

  # Function to normalize and concatenate meta data and line items
  def normalize_and_concatenate_details(row, column_name, prefix):
    if row[column_name]:
      details_df = pd.json_normalize(row[column_name])
      details_df.columns = [
          f'{prefix}_{col.upper()}' for col in details_df.columns
      ]
      for col in details_df.columns:
        row[col] = details_df[col].iloc[
            0] if not details_df[col].empty else None
    return row

  # Normalize META_DATA and LINE_ITEMS for each row
  for column_name, prefix in [('meta_data', 'META'), ('line_items', 'ITEM')]:
    df = df.apply(normalize_and_concatenate_details,
                  axis=1,
                  args=(column_name, prefix))
    df.drop(columns=[column_name], inplace=True)

  # Make all column names uppercase
  df.columns = [col.upper() for col in df.columns]

  # Convert the DataFrame back into a list of dictionaries
  processed_data = df.to_dict('records')
  return processed_data


def fetch_sales_data():
  wc_api = get_wc_api()
  last_timestamp = get_last_processed_timestamp()
  logging.info(f"Starting to fetch sales data after {last_timestamp}")

  page = 1
  per_page = 100
  params = {
      "after":
      last_timestamp.isoformat() if last_timestamp else "2023-01-01T00:00:00",
      "per_page": per_page,
  }

  all_data = []

  try:
    while True:
      params['page'] = page
      response = wc_api.get("orders", params=params)
      logging.info(f"Status code: {response.status_code} for page {page}")

      if response.status_code == 200:
        data = response.json()
        if data:
          all_data.extend(data)
          # Log the number of records fetched
          logging.info(
              f"Fetched {len(data)} records in page {page}. Total records fetched: {len(all_data)}"
          )
          page += 1
        else:
          logging.info(
              "No more sales data to fetch. Successfully completed data fetch."
          )
          break
      else:
        logging.error(
            f"Failed to fetch sales data for page {page}, status code: {response.status_code}"
        )
        break  # Exit the loop on this failure

    if all_data:
      logging.info(f"Fetched a total of {len(all_data)} records.")
    else:
      logging.info("No new sales data to fetch since the last timestamp.")
    return all_data
  except Exception as e:
    logging.error(f"An error occurred while fetching sales data: {e}")

  return None


def fetch_and_process_sales_data():
  sales_data = fetch_sales_data()
  if sales_data is not None:
    if len(sales_data) == 0:
      # Log that there are no sales data to process
      logging.info("No new sales data to process.")
      return None
    processed_data = process_sales_data(sales_data)
    insert_sales_data_to_db(processed_data)
    return processed_data
  else:
    # Log that there was an error fetching sales data
    logging.error("Failed to fetch or process sales data")
    return None


def ingest_woocommerce_data_job():
  logging.info("Fetching sales data...")
  sales_data = fetch_and_process_sales_data()
  if sales_data:
    logging.info("Fetched sales data successfully.")
