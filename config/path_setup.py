import os
import sys


def init_path():
  """Adds the project root directory to sys.path."""
  project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
  if project_root not in sys.path:
    sys.path.append(project_root)


# Call the function immediately upon module import
init_path()
