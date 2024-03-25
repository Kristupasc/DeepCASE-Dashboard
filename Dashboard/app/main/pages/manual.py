import dash
from dash import html, dash_table, dcc, callback, Output, Input
import pandas as pd
import Dashboard.app.main.recources.loaddata as load
import Dashboard.app.main.recources.style as style
from Dashboard.app.main.pagescallback.manual import *

dash.register_page(__name__, path="/manual-analysis", name="Manual Analysis", title="Manual Analysis")

manual_wrapper_style = {
    "background-color": "#E1E7FF",
    "height": "100%",
    "width": "100%",
    "margin": 20
}

layout = html.Div([
    html.H1('Manual Analysis'),
    dcc.Dropdown(
            id="filter_dropdown"+ id_str,
            options=[{"label": st, "value": st} for st in set_cluster],
            placeholder="-Select a State-",
            multi=False,
            value=list(set_cluster)
        ),
    dash_table.DataTable(
        id='manual-analysis',
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
        style_data={
            'width': 'normal', 'minWidth': 'normal', 'maxWidth': 'normal',
            'overflow': 'hidden',
            'textOverflow': 'ellipsis',
        },
        page_size=10),
    # https://dash.plotly.com/datatable/filtering
    # dash_table.DataTable(
    #     id='Context information',
    #     columns=[
    #         {'name': 'Event', 'id': 'Event_ci', 'type': 'numeric', 'hideable': True},
    #         {'name': 'Event_text', 'id': 'event_ci', 'type': 'text', 'hideable': True},
    #         {'name': 'Confident', 'id': 'Context_ci', 'type': 'text'}
    #     ],
    #     data=df.to_dict('records'),
    #     filter_action='native',
    #     style_data={
    #         'width': 'normal', 'minWidth': 'normal', 'maxWidth': 'normal',
    #         'overflow': 'hidden',
    #         'textOverflow': 'ellipsis',
    #     },
    #     page_size=10)
], style=style.content_style)