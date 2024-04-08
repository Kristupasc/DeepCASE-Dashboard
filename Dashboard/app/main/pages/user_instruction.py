import os

import dash
import pandas as pd
from dash import html, dcc, callback, dash_table
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import Dashboard.app.main.recources.style as style

dash.register_page(__name__, path="/user-manual", name="User Manual", title="User Manual", order=0)

with open('../static/User_Manual_Interface_Usage_Guide.md', 'r') as instruction_file:
    instructions = instruction_file.read()
    instruction_file.close()

layout = html.Div(className = 'content', children = [
    html.H1('User Manual: Interface Usage Guide'),
    html.Div(className = 'subcontent user_manual', children = [
        dcc.Markdown(
            instructions
        )
    ])
    ])