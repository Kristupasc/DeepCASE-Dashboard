import dash
from dash import html, dash_table, dcc

import Dashboard.app.main.recources.style as style
from Dashboard.app.main.pagescallback.automated import *
from Dashboard.app.main.pagescallback.display_sequence import *
from dash.dependencies import Input, Output, State


dash.register_page(__name__, path="/semi-automatic", name="Semi-automatic", title="Semi-automatic", order=2)


########################################################################
#   Semi-automatic objects page(Makes use of the callback addition)    #
########################################################################

layout = html.Div(className = 'content', children = [
    html.H1('Semi-automatic'),
    html.Div(className = 'subcontent', children=[
        html.Div(
            style={'display': 'flex', 'alignItems': 'center'},
            children=[
                # html.H2("Cluster:"),
                html.Div(className='dropdown-with-text', children=[
                    html.Label("Select a Cluster:", style={"margin-right": "10px", 'color': 'black'}),
                    dcc.Dropdown(
                        id="filter_dropdown" + id_str,
                        options=update_options_dropdown(0),
                        value=update_values_dropdown(0),
                        clearable=False,
                        placeholder="-Select a Cluster-",
                        multi=False),
                ], id="dropdown_container" + id_str,
                         style={"display": "flex", "align-items": "center", "cursor": "pointer"}
                         ),
                html.H2('Cluster name unknown', id='cluster name' + id_str),
                html.H3('', id="display risk cluster" + id_str,
                        style={'marginLeft': '10px'}),
            ]),


        # ], className='button-with-icon'),

        # Table - cluster data
        dash_table.DataTable(
            id='semi-automatic',
            columns=[
                {'name': 'Date', 'id': 'timestamp' + id_str, 'type': 'text'},
                {'name': 'Source', 'id': 'machine' + id_str, 'type': 'text'},
                {'name': 'Event', 'id': 'id_event' + id_str, 'type': 'numeric', 'hideable': True},
                {'name': 'Event_text', 'id': 'name' + id_str, 'type': 'text', 'hideable': True},
                {'name': 'Risk', 'id': 'risk_label' + id_str, 'type': 'numeric', 'editable': False},
            ],
            # data=df.to_dict('records'),
            filter_action='native',
            row_selectable="single",
            style_data={
                'width': 'normal', 'minWidth': 'normal', 'maxWidth': 'normal',
                'overflow': 'hidden',
                'textOverflow': 'ellipsis',
            },
            page_size=10)],
    ),
    #          )],

    # Context of a sequence
    html.Div(
        className='subcontent',
        children=[
            html.H2('Context of the selected sequence', id='sequence name' + cid_str),
            dash_table.DataTable(
                id='Context information' + cid_str,
                columns=[
                    {'name': 'Position (top oldest)', 'id': 'event_position' + cid_str, 'type': 'numeric',
                     'hideable': True},
                    {'name': 'Event type', 'id': 'event' + cid_str, 'type': 'text', 'hideable': True},
                    {'name': 'Event_name', 'id': 'name' + cid_str, 'type': 'text', 'hideable': True},
                    {'name': 'Attention', 'id': 'attention' + cid_str, 'type': 'text'}
                ],
                # data=df.to_dict('records'),
                filter_action='native',
                style_data={
                    'width': 'normal', 'minWidth': 'normal', 'maxWidth': 'normal',
                    'overflow': 'hidden',
                    'textOverflow': 'ellipsis',
                },

                page_size=10),
            dcc.Interval(
                # This is used for refreshing the dropdown when we enter the page.
                id='refresh-data-automatic',
                interval=500,  # in milliseconds
                n_intervals=0,  # initial value
                max_intervals=1  # maximum number of intervals to fire
            ),
            # Objects to store intermediate values, selected by the above table.
            dcc.Store(id='selected cluster' + id_str),
            dcc.Store(id='selected row' + id_str)
        ],
        # dcc.Store stores the intermediate value
        # style=style.content_style
    ),
]),
    # ])
