import dash
from dash import html, dash_table, dcc, callback, Output, Input
import pandas as pd
import Dashboard.app.main.recources.loaddata as load
import Dashboard.app.main.recources.style as style
dash.register_page(__name__, path="/semi-automatic", name="Semi-automatic", title="Semi-automatic", order=2)
from Dashboard.app.main.pagescallback.automated import *
########################################################################
#   Semi-automatic objects page(Makes use of the callback addition)    #
########################################################################

layout = html.Div([
    html.H1('Semi-automatic'),
    html.H2('cluster name unknown', id='cluster name' + id_str),
    # A signal to update the dropdown menu regularly
    dcc.Interval(
        id='interval' + id_str,
        interval=60 * 1000,  # in milliseconds
        n_intervals=0
    ),
    # drop down menu to select cluster
    dcc.Dropdown(
            id="filter_dropdown"+ id_str,
            options=[{"label": i[1], "value": i[0]} for i in set_cluster],
            placeholder="-Select a Cluster-",
            multi=False,
            value=list([i[0] for i in set_cluster])
        ),

    # data table to display the cluster
    dash_table.DataTable(
        id='semi-automatic',
        columns=[
            {'name': 'Date', 'id': 'timestamp' + id_str, 'type': 'text'},
            {'name': 'Source', 'id': 'machine' + id_str, 'type': 'text'},
            {'name': 'Event', 'id': 'id_cluster'+id_str, 'type': 'numeric', 'hideable': True},
            {'name': 'Event_text', 'id': 'name' + id_str, 'type': 'text', 'hideable': True},
            {'name': 'Risk', 'id': 'risk_label' + id_str, 'type': 'numeric', 'editable': False},
        ],
        data=df.to_dict('records'),
        filter_action='native',
        row_selectable="single",
        style_data={
            'width': 'normal', 'minWidth': 'normal', 'maxWidth': 'normal',
            'overflow': 'hidden',
            'textOverflow': 'ellipsis',
        },
        page_size=10),
    html.H2('Context of the selected event', id='sequence name' + cid_str),
    # Table to show the context of a sequence
    dash_table.DataTable(
        id='Context information'+cid_str,
        columns=[
            {'name': 'Position', 'id': 'event_position'+cid_str, 'type': 'numeric', 'hideable': True},
            {'name': 'event', 'id': 'event'+cid_str, 'type': 'text', 'hideable': True},
            {'name': 'Event_name', 'id': 'name'+cid_str, 'type': 'text', 'hideable': True},
            {'name': 'Attention', 'id': 'attention'+cid_str, 'type': 'text'}
        ],
        data=df.to_dict('records'),
        filter_action='native',

        style_data={
            'width': 'normal', 'minWidth': 'normal', 'maxWidth': 'normal',
            'overflow': 'hidden',
            'textOverflow': 'ellipsis',
        },
        page_size=10),
    # Objects to store intermediate values, selected by the above table.
dcc.Store(id='selected cluster'+ id_str),
dcc.Store(id='selected row'+ id_str)

],
    # dcc.Store stores the intermediate value
    style=style.content_style)
