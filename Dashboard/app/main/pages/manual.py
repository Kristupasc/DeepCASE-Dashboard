import dash
from dash import html, dash_table
import pandas as pd
import Dashboard.app.main.recources.loaddata as load
import Dashboard.app.main.recources.style as style

dash.register_page(__name__, path="/manual-analysis", name="Manual Analysis", title="Manual Analysis", order=1)

df = load.formatSequence()

layout = html.Div([
    html.H1('Manual Analysis'),
    dash_table.DataTable(
        id='manual-analysis',
        columns = [
            {'name': 'Date', 'id':'timestamp', 'type': 'text'},
            {'name': 'Source', 'id':'machine', 'type': 'text'},
            {'name': 'Event', 'id':'Event', 'type': 'numeric', 'hideable': True},
            {'name': 'Event_text', 'id':'event', 'type': 'text', 'hideable': True},
            {'name': 'Risk', 'id':'label', 'type': 'numeric', 'editable': True},
            {'name': 'Context', 'id':'Context', 'type': 'text'}
            ],
        data=df.to_dict('records'),
        filter_action='native',
        style_data={
            'width': 'normal', 'minWidth': 'normal', 'maxWidth': 'normal',
            'overflow': 'hidden',
            'textOverflow': 'ellipsis',
        },
        page_size = 10)
    # https://dash.plotly.com/datatable/filtering


], style=style.content_style)




