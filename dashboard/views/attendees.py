import plotly.express as px
import streamlit as st

from database.db import query_postgresql


def page():
  st.title("Registrations Overview")
  df = query_postgresql()

  st.dataframe(df)