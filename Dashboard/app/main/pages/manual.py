import dash
from dash import html
import Dashboard.app.main.recources.style as style
dash.register_page(__name__, path="/manual-analysis", name="Manual Analysis", title="Manual Analysis", order=1)

layout = html.Div([
    html.H1('Manual Analysis'),
])