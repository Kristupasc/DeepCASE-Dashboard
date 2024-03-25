import dash
from dash import html, dash_table, dcc, callback, Output, Input
import pandas as pd
import Dashboard.app.main.recources.style as style
from dash import html, dash_table, dcc, callback, Output, Input
import Dashboard.app.main.recources.style as style
from Dashboard.app.main.pagescallback.manual import *

import dash

import pandas as pd
import Dashboard.app.main.recources.loaddata as load
dash.register_page(__name__, path="/manual-analysis", name="Manual Analysis", title="Manual Analysis", order=1)


########################################################################
#   Manual objects page(Makes use of the callback addition)    #
########################################################################

layout = html.Div([
    html.H1('Manual'),
    # Change name of cluster and display
    dcc.Textarea(id='cluster name'+id_str, value='Cluster name unknown'),
    html.Button('Change cluster name', id='change cluster name', n_clicks=0),
    html.P(id="set label cluster"+id_str),
    # Get new cluster
    html.Button('Chose next cluster', id='random' + id_str, n_clicks=0),
    # drop down menu to select cluster
    dcc.Dropdown(
        id="filter_dropdown" + id_str,
        options=[{"label": i[1], "value": i[0]} for i in set_cluster],
        placeholder="-Select a Cluster-",
        multi=False,
        value=list([i[0] for i in set_cluster])
    ),

    # data table to display the cluster
    dash_table.DataTable(
        id='manual',
        columns=[
            {'name': 'Date', 'id': 'timestamp' + id_str, 'type': 'text'},
            {'name': 'Source', 'id': 'machine' + id_str, 'type': 'text'},
            {'name': 'Event', 'id': 'id_event' + id_str, 'type': 'numeric', 'hideable': True},
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
    ################## Editable risk values
    html.Button('Chose next sequence', id='random' + qid_str, n_clicks=0),
    html.H3(id='doneCluster' + qid_str),
    html.H3("Event to be labeled."),
    dash_table.DataTable( id='chosen sequence manual',
        columns=[
            {'name': 'Date', 'id': 'timestamp' + qid_str, 'type': 'text'},
            {'name': 'Source', 'id': 'machine' + qid_str, 'type': 'text'},
            {'name': 'Event', 'id': 'id_event' + qid_str, 'type': 'numeric', 'hideable': True},
            {'name': 'Event_text', 'id': 'name' + qid_str, 'type': 'text', 'hideable': True},
            {'name': 'Risk', 'id': 'risk_label' + qid_str, 'type': 'numeric', 'editable': False},
        ],
        data=(pd.DataFrame()).to_dict('records'),
        filter_action='native',
        style_data={
            'width': 'normal', 'minWidth': 'normal', 'maxWidth': 'normal',
            'overflow': 'hidden',
            'textOverflow': 'ellipsis',
        },
        page_size=10),
    dcc.Input(placeholder='risk label', id='risk_label' + qid_str, type='number', step=1),
    html.Button('Submit change', id='submit' + qid_str, n_clicks=0),
    html.H3(id="successful"+qid_str),



    ################## Display context
    html.H2('Context of the selected sequence', id='sequence name' + cid_str),
    # Table to show the context of a sequence
    dash_table.DataTable(
        id='Context information' + cid_str,
        columns=[
            {'name': 'Position(top old, bottom newest)', 'id': 'event_position' + cid_str, 'type': 'numeric', 'hideable': True},
            {'name': 'event', 'id': 'event' + cid_str, 'type': 'text', 'hideable': True},
            {'name': 'Event_name', 'id': 'name' + cid_str, 'type': 'text', 'hideable': True},
            {'name': 'Attention', 'id': 'attention' + cid_str, 'type': 'text'}
        ],
        data=(pd.DataFrame()).to_dict('records'),
        filter_action='native',

        style_data={
            'width': 'normal', 'minWidth': 'normal', 'maxWidth': 'normal',
            'overflow': 'hidden',
            'textOverflow': 'ellipsis',
        },
        page_size=10),
    # Objects to store intermediate values, selected by the above table.
    dcc.Store(id='selected cluster' + id_str),
    dcc.Store(id='selected row' + id_str)

],
    # dcc.Store stores the intermediate value
    style=style.content_style)
