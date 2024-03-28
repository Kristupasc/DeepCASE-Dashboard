import dash
from dash import html, dash_table, dcc, callback, Output, Input
import pandas as pd
import Dashboard.app.main.recources.loaddata as load
import Dashboard.app.main.recources.style as style
dash.register_page(__name__, path="/semi-automatic", name="Semi-automatic", title="Semi-automatic", order=2)
from Dashboard.app.main.pagescallback.automated import *


layout = html.Div(className="app-header",
    children=[
    html.H1('Semi-automatic'),
    dcc.Dropdown(
            id="filter_dropdown"+ id_str,
            options=[{"label": st, "value": st} for st in set_cluster],
            placeholder="-Select a State-",
            multi=False,
            value=list(set_cluster)
        ),
    dash_table.DataTable(
        id='semi-automatic',
        columns=[
            {'name': 'Date', 'id': 'timestamp' + id_str, 'type': 'text'},
            {'name': 'Source', 'id': 'machine' + id_str, 'type': 'text'},
            {'name': 'Event', 'id': 'Event'+ id_str, 'type': 'numeric', 'hideable': True},
            {'name': 'Event_text', 'id': 'event' + id_str, 'type': 'text', 'hideable': True},
            {'name': 'Risk', 'id': 'labels' + id_str, 'type': 'numeric', 'editable': True},
            {'name': 'Context', 'id': 'Context'+ id_str, 'type': 'text'}
        ],
        data=df.to_dict('records'),
        filter_action='native',
        style_data=style.table_data,
        style_header=style.table_header,
        style_cell=style.table_cell,
        page_size=10),
    # https://dash.plotly.com/datatable/filtering
    dash_table.DataTable(
        id='Context information'+cid_str,
        columns=[
            {'name': 'Event', 'id': 'Event'+cid_str, 'type': 'numeric', 'hideable': True},
            {'name': 'Event_text', 'id': 'event'+cid_str, 'type': 'text', 'hideable': True},
            {'name': 'Confident', 'id': 'Context'+cid_str, 'type': 'text'}
        ],
        data=df.to_dict('records'),
        filter_action='native',
        style_data=style.table_data,
        style_header=style.table_header,
        style_cell=style.table_cell,
        page_size=10),
    # style = style.table_style
], style=style.content_style)
