import os
import sys

import dash
import plotly.express as px
from dash import dcc, html
from dash.dependencies import Input, Output

# Add the parent directory to the system path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

from database.db import get_db_data_for_dashboard

# Initialize the Dash app
app = dash.Dash(__name__)
app.layout = html.Div([
    dcc.Graph(id='registration-graph'),
    dcc.Interval(
        id='interval-component',
        interval=1 * 60000,  # in milliseconds
        n_intervals=0)
])


@app.callback(Output('registration-graph', 'figure'),
              [Input('interval-component', 'n_intervals')])
def update_graph(n):
  # Fetch data from the database using the implemented function
  df = get_db_data_for_dashboard()
  # Create a line chart using Plotly Express
  fig = px.line(df, x='Date', y='Registrations', title='Daily Registrations')
  return fig


if __name__ == '__main__':
  app.run_server(debug=True)
