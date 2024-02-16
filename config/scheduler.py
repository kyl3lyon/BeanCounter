import logging
import time

import schedule

from config.logs import setup_logging
from main import ingest_woocommerce_data_job

# Call the logging setup to ensure that log messages are configured properly
setup_logging()


def setup_schedule():
  # Run the job immediately first.
  ingest_woocommerce_data_job()

  # Schedule the job to run at the top of every hour
  schedule.every().hour.at(":00").do(ingest_woocommerce_data_job)
  # Log that the scheduler has started.
  logging.info(
      "Scheduler started, running the ingestion job immediately and then every top of the hour."
  )

  # Execute the scheduled jobs indefinitely.
  while True:
    schedule.run_pending()
    time.sleep(1)  # Wait for one second before checking the schedule again
    # Adds a log statement that confirms the scheduler is running, every 10 minutes.
    if int(time.strftime('%M')) % 10 == 0:  # Every 10 minutes
      logging.info("Scheduler is running, waiting for the next job...")


if __name__ == "__main__":
  setup_schedule()
