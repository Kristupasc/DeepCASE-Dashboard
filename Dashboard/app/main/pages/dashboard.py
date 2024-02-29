import dash
from dash import html

dash.register_page(__name__, path="/", name="Dashboard", title="Dashboard", order=0)

layout = html.Div([
    html.H1('Dashboard')
])