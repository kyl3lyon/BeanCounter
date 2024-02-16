import os
from datetime import datetime

import pandas as pd
from woocommerce import API

from config.settings import (
    WOO_COMMERCE_CONSUMER_KEY,
    WOO_COMMERCE_CONSUMER_SECRET,
    WOO_COMMERCE_URL,
)
from database.db import get_last_processed_timestamp, insert_sales_data_to_db


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

  # Define the 'after' parameter to fetch orders after January 1, 2023
  params = {
      "after":
      last_timestamp.isoformat() if last_timestamp else "2023-01-01T00:00:00",
      "per_page": 100  # Default is 10
  }
  response = wc_api.get("orders", params=params)
  if response.status_code == 200:
    return response.json()
  else:
    return None


def fetch_and_process_sales_data():
  sales_data = fetch_sales_data()
  if sales_data is not None:
    processed_data = process_sales_data(sales_data)
    # Invoke the function to insert the data into the database
    insert_sales_data_to_db(processed_data)
    return processed_data
  else:
    print("Failed to fetch sales data")
