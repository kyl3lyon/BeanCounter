import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from database.db import query_postgresql


def page():
  st.title("Attendees Overview")
  df = query_postgresql()

  # ---- Quick Facts Section ----
  st.subheader("Quick Facts")
  col1, col2 = st.columns(2)
  col1.metric("Total Registrations", len(df))
  # Format revenue as dollars
  total_revenue = "${:,.2f}".format(df['item_total'].sum())
  col2.metric("Total Revenue", total_revenue)

  # Creating two columns for the charts
  col1, col2 = st.columns(2)

  with col1:
    # ---- Bar Chart of Items Purchased ----
    st.subheader("Top Grossing Registration Types")
    # Short description under the subtitle
    st.write("Products ranked by total revenue generated.")

    # Grouping, aggregating, and sorting by total revenue before formatting for display
    top_items = df.groupby('item_name').agg(
        item_count=pd.NamedAgg(column='item_name', aggfunc='count'),
        total_revenue=pd.NamedAgg(column='item_total',
                                  aggfunc='sum')).reset_index()

    # Sorting by total revenue in descending order to get the top items by revenue
    top_items = top_items.nlargest(10, 'total_revenue')

    # Formatting the total revenue for display after sorting
    top_items['total_revenue'] = top_items['total_revenue'].apply(
        lambda x: "${:,.2f}".format(x))

    # Creating the bar chart sorted by total revenue
    fig = px.bar(top_items,
                 x='item_name',
                 y='total_revenue',
                 hover_data=['item_count'],
                 labels={
                     'item_count': 'Count',
                     'item_name': 'Item Name',
                     'total_revenue': 'Revenue ($)'
                 })

    # Adjusting y-axis to represent total revenue
    fig.update_yaxes(title='Total Revenue')
    st.plotly_chart(fig)

  with col2:
    # ---- Timeline of Purchases ----
    st.subheader("Purchases by Item Over Time")

    # Short description under the subtitle
    st.write(
        "This chart displays the top 10 purchased items ranked by total revenue generated, providing insights into the most profitable items."
    )

    df['date_created'] = pd.to_datetime(
        df['date_created'])  # Ensure date_created is datetime
    fig = px.line(df,
                  x='date_created',
                  y='item_quantity',
                  color='item_name',
                  labels={
                      'item_quantity': 'Quantity',
                      'date_created': 'Date'
                  })
    st.plotly_chart(fig)

  # ---- Detailed Customer Table ----
  st.subheader("Customer Details")
  display_columns = [
      'date_created', 'order_id', 'billing_first_name', 'billing_last_name',
      'billing_email', 'billing_phone', 'item_name', 'item_total'
  ]  # Adapt columns as needed
  st.dataframe(df[display_columns],
               use_container_width=True)  # Adjusted for full width
