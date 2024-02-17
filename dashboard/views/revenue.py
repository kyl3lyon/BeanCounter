import plotly.express as px
import streamlit as st

from database.db import query_postgresql


def page():
  st.title("Revenue Overview")
  df = query_postgresql()
  fig = px.line(df, x='Date', y='Regaistrations', title='Daily Registrations')
  st.plotly_chart(fig)
