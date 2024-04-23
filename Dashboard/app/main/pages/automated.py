import dash
from dash import html, dash_table, dcc

# Importing styles and callback functions
from Dashboard.app.main.pagescallback.automated import *
from Dashboard.app.main.pagescallback.common import *

# Registering the page with Dash
dash.register_page(__name__, path="/semi-automatic", name="Semi-automatic", title="Semi-automatic", order=2)
########################################################################
#               Automatic analysis page                                #
########################################################################
# Layout definition for the semi-automatic dashboard page
layout = html.Div(className='content', children=[
    html.H1('Semi-automatic'),  # Main heading of the page

    # Sub-content division containing components
    html.Div(className='subcontent', children=[
        # Division for displaying cluster information

        html.Div(
            style={'display': 'flex', 'alignItems': 'center'},
            children=[
                html.Div(className='dropdown-with-text', children=[
                    html.Label("Select a Cluster:", style={"margin-right": "10px", 'color': 'black'}),
                    dcc.Dropdown(
                        id="filter_dropdown" + id_str,
                        options=update_options_dropdown(0),
                        clearable=False,
                        multi=False,
                        value=update_values_dropdown(0),
                    ),
                ], style={"display": "flex", "align-items": "center", "cursor": "pointer"}),

                html.H2("Cluster:"),  # Heading for cluster information
                html.H2('Cluster name unknown', id='cluster name' + id_str),  # Display cluster name
                html.H3('', id="display risk cluster" + id_str, style={'marginLeft': '10px'}),
                # Display risk information
            ]),

        # Table to display cluster data
        dash_table.DataTable(
            id='semi-automatic',
            columns=[
                {'name': 'Date', 'id': 'timestamp' + id_str, 'type': 'text'},
                {'name': 'Source', 'id': 'machine' + id_str, 'type': 'text'},
                {'name': 'Event', 'id': 'id_event' + id_str, 'type': 'numeric', 'hideable': True},
                {'name': 'Event_text', 'id': 'name' + id_str, 'type': 'text', 'hideable': True},
                {'name': 'Risk', 'id': 'risk_label' + id_str, 'type': 'numeric', 'editable': False},
            ],
            filter_action='native',
            row_selectable="single",
            style_data={
                'width': 'normal', 'minWidth': 'normal', 'maxWidth': 'normal',
                'overflow': 'hidden',
                'textOverflow': 'ellipsis',
            },
            page_size=10)
    ]),

    # Context information of selected sequence
    html.Div(
        className='subcontent',
        children=[
            html.H2('Context of the selected sequence', id='sequence name' + cid_str),
            # Heading for context information

            # Table to display context information
            dash_table.DataTable(
                id='Context information' + cid_str,
                columns=[
                    {'name': 'Position (top oldest)', 'id': 'event_position' + cid_str, 'type': 'numeric',
                     'hideable': True},
                    {'name': 'Event type', 'id': 'event' + cid_str, 'type': 'text', 'hideable': True},
                    {'name': 'Event_name', 'id': 'name' + cid_str, 'type': 'text', 'hideable': True},
                    {'name': 'Attention', 'id': 'attention' + cid_str, 'type': 'text'}
                ],
                filter_action='native',
                style_data={
                    'width': 'normal', 'minWidth': 'normal', 'maxWidth': 'normal',
                    'overflow': 'hidden',
                    'textOverflow': 'ellipsis',
                },
                page_size=10),

            # Interval component for refreshing dropdown
            dcc.Interval(
                id='refresh-data-automatic',
                interval=500,  # in milliseconds
                n_intervals=0,  # initial value
                max_intervals=1  # maximum number of intervals to fire
            ),

            # Objects to store intermediate values selected by the above table
            dcc.Store(id='selected cluster' + id_str),
            dcc.Store(id='selected row' + id_str)
        ],
    ),
])
# ])
