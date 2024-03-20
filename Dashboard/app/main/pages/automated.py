import dash
from dash import html, dash_table, dcc, callback, Output, Input
import pandas as pd
import Dashboard.app.main.recources.loaddata as load
import Dashboard.app.main.recources.style as style
dash.register_page(__name__, path="/semi-automatic", name="Semi-automatic", title="Semi-automatic", order=2)
from Dashboard.app.main.pagescallback.automated import *




layout = html.Div([
    html.H1('Semi-automatic')])
