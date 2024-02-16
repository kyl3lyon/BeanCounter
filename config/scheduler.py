import time

import schedule

from main import fetch_sales_data_job


def setup_schedule():
  # Schedule the fetch_sales_data_job to run at the top of every hour
  schedule.every().hour.at(":00").do(fetch_sales_data_job)
  # Execute the scheduled job
  while True:
      schedule.run_pending()
      time.sleep(1)
if __name__ == "__main__":
  setup_schedule()