import os

import dash
import pandas as pd
from dash import html, dcc, callback, dash_table
from dash.dependencies import Input, Output, State
from Dashboard.data import dummyData, createDf
import plotly.graph_objs as go
import Dashboard.app.main.recources.style as style
# create csv x2
# upload through database
# make it cluster on dashboard

GRAPH_INTERVAL = os.environ.get("GRAPH_INTERVAL", 5000)

dash.register_page(__name__, path="/", name="Dashboard", title="Dashboard", order=0)

# Define color scheme
colors = {
    "background": "#FFFFFF",  # white background
    "text": "#000000",  # black text for visibility
    "Risk Label": {
        "Info": "#45B6FE",  # blue
        "Low": "#FFD700",  # gold
        "Medium": "#FF8C00",  # darkorange
        "High": "#FF4500",  # orangered
        "Attack": "#DC143C",  # crimson
        "Suspicious": "#800080",  # purple
        "Unlabeled": "#808080"  # grey
    }
}


layout = html.Div([
    html.H1('Dashboard'),
], style=style.content_style)


