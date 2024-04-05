import Dashboard.app.main.recources.style as style
from Dashboard.app.main.pagescallback.dashboard import *
from Dashboard.app.main.pagescallback.display_sequence import *
from dash import html, dcc, dash_table
import dash

dash.register_page(__name__, path="/dashboard", name="Dashboard", title="Dashboard", order=0)

########################################################################
#               Cluster View page (the main dashboard).                #
########################################################################

layout = html.Div([
    # TOP SECTION
    html.Div(children=[
        html.H1('Cluster view'),
        # Change name of file and display
        dcc.Textarea(id='filename' + id_str, value='File not selected'),
        html.Button('Change filename', id='change filename' + id_str, n_clicks=0),
        dcc.Dropdown(
            id="filename_dropdown" + id_str,
            placeholder="-Select a file-",
            multi=False,
            clearable=False,
        ),
        html.H2('cluster name unknown', id='cluster name' + id_str),
        # drop down menu to select cluster
        dcc.Dropdown(
            id="filter_dropdown" + id_str,
            options=update_options_dropdown(None),
            value=update_values_dropdown(None),
            placeholder="-Select a Cluster-",
            clearable=False,
            multi=False,
        ),
        html.H3('Security label cluster:'),
        html.H3('8', id="display risk cluster" + id_str),
        # data table to display the cluster
        dash_table.DataTable(
            id='dashboard',
            columns=[
                {'name': 'Date', 'id': 'timestamp' + id_str, 'type': 'text'},
                {'name': 'Source', 'id': 'machine' + id_str, 'type': 'text'},
                {'name': 'Event', 'id': 'id_event' + id_str, 'type': 'numeric', 'hideable': True},
                {'name': 'Event_text', 'id': 'name' + id_str, 'type': 'text', 'hideable': True},
                {'name': 'Risk', 'id': 'risk_label' + id_str, 'type': 'numeric'},
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
        html.Div(className='semiauto_context', children=[
            html.H2('Context of the selected sequence', id='sequence name' + cid_str),

            # Table to show the context of a sequence
            dash_table.DataTable(
                id='Context information' + cid_str,
                columns=[
                    {'name': 'Position(top oldest)', 'id': 'event_position' + cid_str, 'type': 'numeric',
                     'hideable': True},
                    {'name': 'Event', 'id': 'event' + cid_str, 'type': 'text', 'hideable': True},
                    {'name': 'Event_type', 'id': 'name' + cid_str, 'type': 'text', 'hideable': True},
                    {'name': 'Attention', 'id': 'attention' + cid_str, 'type': 'text'}
                ],
                # data=df.to_dict('records'),
                filter_action='native',
                style_data={
                    'width': 'normal', 'minWidth': 'normal', 'maxWidth': 'normal',
                    'overflow': 'hidden',
                    'textOverflow': 'ellipsis',
                },
                page_size=10)], style={'background-color': 'red'}),
    ], style=style.content_style
    ),

    # BOTTOM SECTION - Sequences graph
    html.Div(className='cluster_sequences_graph', children=[
        # Buttons to filter the scatter plot
        dcc.RadioItems(
            id='filter-buttons',
            options=[
                {'label': 'All', 'value': 'All'},
                {'label': 'Info', 'value': 'Info'},
                {'label': 'Low', 'value': 'Low'},
                {'label': 'Medium', 'value': 'Medium'},
                {'label': 'High', 'value': 'High'},
                {'label': 'Attack', 'value': 'Attack'},
                {'label': 'Unlabeled', 'value': 'Unlabeled'},
                {'label': 'Custom', 'value': 'Custom'}
            ],
            value='all',  # Default value
            labelStyle={'display': 'inline-block'}
        ),

        # Graph to display the scatter plot
        html.Div(children=[html.H2("All Sequences in Cluster", className="graph__title"),
                           dcc.Graph(id="scatter-plot"),
                           dcc.Interval(
                               id="scatter-update",
                               interval=int(5000),
                               n_intervals=0,
                           ),
                           ],
                 ), ]
             ),

    # Objects to store intermediate values, selected by the above table.
    dcc.Store(id='selected cluster' + id_str),
    dcc.Store(id='selected row' + id_str),

],
)
