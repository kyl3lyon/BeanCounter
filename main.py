from api.woocommerce import fetch_and_process_sales_data


def main():
  sales_data = fetch_and_process_sales_data()
  if sales_data is not None:
    print("Fetched sales data successfully:")
  else:
    print("Failed to fetch sales data")


if __name__ == "__main__":
  main()
