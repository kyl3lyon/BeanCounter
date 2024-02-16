import logging
import os


def setup_logging():
  log_dir = "logs"
  if not os.path.exists(log_dir):
    os.makedirs(log_dir)

  log_file_path = os.path.join(log_dir, "application.log")

  logging.basicConfig(
      level=logging.INFO,
      format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
      handlers=[
          logging.StreamHandler(),
          logging.FileHandler(log_file_path, mode='a')
      ])
