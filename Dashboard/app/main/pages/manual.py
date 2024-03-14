import dash
from dash import html, dash_table,dcc
import pandas as pd
import Dashboard.app.main.recources.loaddata as load
import Dashboard.app.main.recources.style as style

dash.register_page(__name__, path="/manual-analysis", name="Manual Analysis", title="Manual Analysis", order=1)

df = load.formatSequenceCluster(0, "_ma")
set_cluster = load.possible_clusters()
layout = html.Div([
    html.H1('Manual Analysis'),
    dcc.Dropdown(
            id="filter_dropdown_ma",
            options=[{"label": st, "value": st} for st in set_cluster],
            placeholder="-Select a State-",
            multi=False,
            value=list(set_cluster)
        ),
    dash_table.DataTable(
        id='manual-analysis',
        columns=[
            {'name': 'Date', 'id': 'timestamp_ma', 'type': 'text'},
            {'name': 'Source', 'id': 'machine_ma', 'type': 'text'},
            {'name': 'Event', 'id': 'Event_ma', 'type': 'numeric', 'hideable': True},
            {'name': 'Event_text', 'id': 'event_ma', 'type': 'text', 'hideable': True},
            {'name': 'Risk', 'id': 'labels_ma', 'type': 'numeric', 'editable': True},
            {'name': 'Context', 'id': 'Context_ma', 'type': 'text'}
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
