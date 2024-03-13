import dash
from dash import html
import Dashboard.app.main.recources.style as style
dash.register_page(__name__, path="/ai-analysis", name="AI Analysis", title="AI Analysis", order=2)

layout = html.Div([
    html.H1('AI Analysis'),
])