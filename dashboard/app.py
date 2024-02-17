import os
import sys
from datetime import datetime, timedelta

import plotly.express as px
import streamlit as st

# Ensure the parent directory is in the system path for module imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

from database.db import get_db_data_for_dashboard


# Function to simulate live data updates
def update_graph():
  df = get_db_data_for_dashboard()
  fig = px.line(df, x='Date', y='Registrations', title='Daily Registrations')
  st.plotly_chart(fig)


# Streamlit app layout
st.title('Dashboard')
st.write('This dashboard updates every minute with new registration data.')

# Display the graph
update_graph()


# Use Streamlit's caching to only reload data every minute
@st.cache(ttl=60)
def get_cached_data():
  return get_db_data_for_dashboard()


# Schedule data updates
last_update = st.session_state.get('last_update', None)
current_time = datetime.now()

if last_update is None or current_time - last_update > timedelta(minutes=1):
  st.session_state['last_update'] = current_time
  df = get_cached_data()
  fig = px.line(df, x='Date', y='Registrations', title='Daily Registrations')
  st.plotly_chart(fig)
