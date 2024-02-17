import json
import subprocess
from multiprocessing import Process, set_start_method

from config.logs import setup_logging
from config.scheduler import setup_schedule
from config.settings import STREAMLIT_APP_PATH


def run_streamlit_app():
  if STREAMLIT_APP_PATH:
    streamlit_command = f"streamlit run {STREAMLIT_APP_PATH}"
    subprocess.run(streamlit_command, shell=True)
  else:
    raise EnvironmentError("Streamlit app path is not set in settings.py.")


def run_scheduler():
  setup_schedule()


class ProcessManager:
  # Set the start method to "fork" to ensure that the child processes are created
  def __init__(self, target, args=None):
    if args is None:
      self.process = Process(target=target)
    else:
      self.process = Process(target=target, args=args)

  # Start the process
  def __enter__(self):
    self.process.start()
    return self.process

  # Stop the process
  def __exit__(self, exc_type, exc_val, exc_tb):
    self.process.join()


def main():
  # Ensure the default start method is appropriate for the platform
  set_start_method('spawn')
  setup_logging()

  with ProcessManager(run_scheduler), ProcessManager(run_streamlit_app):
    # Both processes are started, and we wait for them to complete.
    # This block ensures that any cleanup logic is executed upon exiting.
    pass  # You can perform other main thread tasks here, if necessary.


if __name__ == "__main__":
  main()
