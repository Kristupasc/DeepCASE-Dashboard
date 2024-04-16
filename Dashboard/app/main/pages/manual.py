import dash
import dash_mantine_components as dmc
import pandas as pd
from dash import html, dash_table, dcc

from Dashboard.app.main.pagescallback.display_sequence import update_options_dropdown, update_values_dropdown
from Dashboard.app.main.pagescallback.manual import *

dash.register_page(__name__, path="/manual-analysis", name="Manual Analysis", title="Manual Analysis", order=1)

########################################################################
#   Manual objects page(Makes use of the callback addition)            #
########################################################################
layout = html.Div(className='content', children=[
    html.H1('Manual analysis'),
    html.P(id="set label cluster" + id_str),
    html.Div(className="subcontent top-bar", children=[
        # Start automatic analysis.
        html.Button(
            [
                html.Img(src='/assets/start-icon.svg', className="icon"),
                html.H3(id='feedback automatic'),
                html.Div('Start semi-automatic analysis', id='start automatic', n_clicks=0),
            ], className='button-with-icon'
        ),
    ]),

    html.Div(className='subcontent', children=[
        # Objects to display the risk value of the cluster.
        html.Div(
            style={'display': 'flex', 'alignItems': 'center'},
            children=[
                html.H2("Cluster: "),
                dcc.Textarea(id='cluster name' + id_str, value='Cluster name unknown'),
                html.H3('', id="display risk cluster" + id_str,
                        style={'marginLeft': '10px'}),
            ]),
        html.Div(className='top-bar', children=[
            html.Div(className='dropdown-with-text', children=[
                html.Label("Select a Cluster:", style={"margin-right": "10px", 'color': 'black'}),
                dcc.Dropdown(
                    id="filter_dropdown" + id_str,
                    options=update_options_dropdown(0),
                    # placeholder="-Select a Cluster-",
                    clearable=False,
                    multi=False,
                    value=update_values_dropdown(0),
                ),
            ], style={"display": "flex", "align-items": "center", "cursor": "pointer"}),

            html.Button(
                [
                    html.Img(src='/assets/pencil-svgrepo-com.svg', className="icon"),
                    html.Div('Change cluster name', id='change cluster name', n_clicks=0),
                ], className='button-with-icon'
            ),
            # Get new cluster
            html.Button(
                [
                    html.Img(src='/assets/random-dice.svg', className="icon"),
                    html.Div('Choose random cluster', id='random' + id_str, n_clicks=0),
                ], className='button-with-icon'
            ),
            html.Button(
                [
                    html.Img(src='/assets/random-dice.svg', className="icon"),
                    html.Div('Choose random sequence', id='random' + qid_str, n_clicks=0),
                ], className='button-with-icon'
            ),
            # Get new cluster
            html.Button(
                [
                    html.Img(src='/assets/random-dice.svg', className="icon"),
                    html.Div('Choose next cluster', id='next' + id_str, n_clicks=0),
                ], className='button-with-icon'
            ),
            html.Button(
                [
                    html.Img(src='/assets/random-dice.svg', className="icon"),
                    html.Div('Choose next sequence', id='next' + qid_str, n_clicks=0),
                ], className='button-with-icon'
            ),
            html.H3(id='doneCluster' + qid_str),
            html.H3(id="successful" + qid_str),
        ]),

        # data table to display the cluster
        html.Div(className='sequences_table subcontent', children=[
            html.H2('Sequences within cluster'),
            dash_table.DataTable(
                id='manual',
                # renamable=True,
                # editable=True,
                columns=[
                    {'name': 'Date', 'id': 'timestamp' + id_str, 'type': 'text'},
                    {'name': 'Source', 'id': 'machine' + id_str, 'type': 'text'},
                    {'name': 'Event', 'id': 'id_event' + id_str, 'type': 'numeric', 'hideable': True},
                    {'name': 'Event_text', 'id': 'name' + id_str, 'type': 'text', 'hideable': True},
                    {'name': 'Risk', 'id': 'risk_label' + id_str, 'type': 'numeric', 'editable': True},
                ],
                # data=df.to_dict('records'),
                filter_action='native',
                row_selectable="single",
                style_data={
                    'width': 'normal', 'minWidth': 'normal', 'maxWidth': 'normal',
                    'overflow': 'hidden',
                    'textOverflow': 'ellipsis',
                },
                page_size=10),
            ################## Editable risk values
            # html.Button('Choose random sequence', id='random' + qid_str, n_clicks=0),
            html.H3(id='doneCluster' + qid_str),
            html.Button(
                [
                    html.Img(src='/assets/change-icon.svg', className="icon"),
                    html.Div('Apply change', id='submit' + qid_str, n_clicks=0),
                ], className='button-with-icon'
            ),
            html.H3(id="successful" + qid_str),
        ], ),
        # style={"display": "flex"}),

        ## Selected sequence context
        html.Div(className='subcontent', children=[
            html.H2('Context of the selected sequence', id='sequence name' + cid_str),
            # Table to show the context of a sequence
            dash_table.DataTable(
                id='Context information' + cid_str,
                columns=[
                    {'name': 'Position(top old, bottom newest)', 'id': 'event_position' + cid_str, 'type': 'numeric',
                     'hideable': True},
                    {'name': 'Event', 'id': 'event' + cid_str, 'type': 'text', 'hideable': True},
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
            dcc.Store(id='selected row' + id_str),
            dcc.Store(id="process of automatic" + id_str)

        ]),
        dmc.Modal(title="Yeeeeeeeeaaaaaaaa", id="modal_set_cluster" + id_str),
        dmc.Modal(title="Noooooooo", id="modal_set_risk" + id_str),
        dmc.Modal(title="Ahhhh", id="feedback start automatic" + id_str),
    ],
             )
])
