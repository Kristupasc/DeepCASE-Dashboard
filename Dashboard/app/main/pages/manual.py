import dash
from dash import html, dash_table, dcc, callback, Output, Input
import pandas as pd
import Dashboard.app.main.recources.loaddata as load
import Dashboard.app.main.recources.style as style
from Dashboard.app.main.pagescallback.manual import *
dash.register_page(__name__, path="/manual-analysis", name="Manual Analysis", title="Manual Analysis", order=1)

layout = html.Div([
    html.H1('Manual Analysis'),
    ], style=style.content_style)

