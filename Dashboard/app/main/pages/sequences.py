import dash
from dash import html, dash_table
import pandas as pd
import Dashboard.app.main.pages.loaddata as load

dash.register_page(__name__, path="/sequences", name="Sequences", title="Sequences", order=5)

layout = html.Div([
    html.H1('Sequence'),

])
df = load.concatTwoFiles('../../data/sequences.csv','../../data/alerts.csv')
dash_table.DataTable(data=df.to_dict('records'), page_size = 10)





