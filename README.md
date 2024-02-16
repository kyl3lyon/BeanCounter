# Bean Counter

Bean Counter is an automated data ingestion system designed to fetch and process WooCommerce sales data, and insert the processed data into a PostgreSQL database. This Python-based system integrates with the WooCommerce API to periodically retrieve sales information, normalize and enrich the data, and then store it efficiently for further analysis.

## Features

* Automated Sales Data Fetching: Connects to the WooCommerce API to fetch sales data.
* Data Processing: Normalizes and processes the raw sales data for easier analysis.
* Database Integration: Inserts processed data into a PostgreSQL database.
* Logging: Comprehensive logging for tracking the application's operations and troubleshooting issues.
* Retry Mechanism: Implements a retry mechanism for API calls to handle temporary network or API issues.
* Scheduling: Automatically schedules data fetching jobs to run at the top of every hour.
