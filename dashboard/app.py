import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st

from dashboard.views.attendees import page as attendees_overview
from dashboard.views.presenters import page as presenter_overview
from dashboard.views.revenue import page as revenue_overview

# Page Configuration
st.set_page_config(page_title="2024 ICSB Registrations Dashboard",
                   layout="wide")

# Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Select a View",
    ["Attendee Overview", "Presenter Overview", "Revenue Overview"])

if page == "Attendee Overview":
  attendees_overview()
elif page == "Presenter Overview":
  presenter_overview()
elif page == "Revenue Overview":
  revenue_overview()
