from datetime import datetime, timezone

import pandas as pd
import psycopg2
import streamlit as st

from config.settings import DATABASE_URL


def get_db_connection():
  return psycopg2.connect(DATABASE_URL)


def get_last_processed_timestamp():
  with get_db_connection() as conn, conn.cursor() as cursor:
    cursor.execute("SELECT MAX(processed_timestamp) FROM sales_data;")
    result = cursor.fetchone()
  return result[0] if result[0] else datetime.min.replace(tzinfo=timezone.utc)


def insert_sales_data_to_db(processed_data):
  conn = get_db_connection()
  cursor = conn.cursor()

  query = """
  INSERT INTO sales_data (
      order_id, parent_id, status, currency, total, date_created, date_modified,
      customer_id, payment_method, customer_ip_address, customer_user_agent,
      payment_url, link_self, link_collection, billing_first_name, billing_last_name,
      billing_email, billing_phone, item_name, item_product_id, item_quantity,
      item_total, item_image_src, processed_timestamp
  ) VALUES (
      %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
      %s, %s, %s, %s, %s
  ) ON CONFLICT (order_id)
  DO NOTHING;
  """

  for record in processed_data:
    values = (record['ID'], record['PARENT_ID'], record['STATUS'],
              record['CURRENCY'], record['TOTAL'], record['DATE_CREATED'],
              record['DATE_MODIFIED'], record['CUSTOMER_ID'],
              record['PAYMENT_METHOD'], record['CUSTOMER_IP_ADDRESS'],
              record['CUSTOMER_USER_AGENT'], record['PAYMENT_URL'],
              record['LINK_SELF'], record['LINK_COLLECTION'],
              record['BILLING_FIRST_NAME'], record['BILLING_LAST_NAME'],
              record['BILLING_EMAIL'], record['BILLING_PHONE'],
              record['ITEM_NAME'], record['ITEM_PRODUCT_ID'],
              record['ITEM_QUANTITY'], record['ITEM_TOTAL'],
              record['ITEM_IMAGE.SRC'], datetime.now(timezone.utc))
    cursor.execute(query, values)

  conn.commit()
  cursor.close()
  conn.close()


@st.cache_data
def query_postgresql():
  conn = get_db_connection()
  try:
    sql_query = """
      SELECT *
      FROM sales_data
      WHERE date_created > '2023-01-01T00:00:00'
      AND status != 'failed'
      ORDER BY date_created DESC;
      """
    df = pd.read_sql_query(sql_query, conn)
    return df
  except Exception as e:
    print(f"An error occurred: {e}")
    return pd.DataFrame()  # Return an empty DataFrame on error
  finally:
    conn.close()
