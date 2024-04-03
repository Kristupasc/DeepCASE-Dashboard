import Dashboard.app.main.recources.style as style
from Dashboard.app.main.pagescallback.manual import *
import dash_mantine_components as dmc
dash.register_page(__name__, path="/manual-analysis", name="Manual Analysis", title="Manual Analysis", order=1)

########################################################################
#   Manual objects page(Makes use of the callback addition)    #
########################################################################

layout = html.Div([
    html.Div([

    dcc.Dropdown(
        id="filter_dropdown" + id_str,
        # options=[{"label": i[1], "value": i[0]} for i in set_cluster],
        placeholder="-Select a Cluster-",
        multi=False,
        clearable=False,
        # value=list([i[0] for i in set_cluster])
    ),
    html.H1('Manual analysis'),
], style={'display': 'flex', 'align-items': 'center'}),
    # Change name of cluster and display
    dcc.Textarea(id='cluster name' + id_str, value='Cluster name unknown'),
    html.Button('Change cluster name', id='change cluster name', n_clicks=0),
    # Get new cluster
    html.Button('Choose random cluster', id='random' + id_str, n_clicks=0),
    html.Button('Choose next sequence', id='random' + qid_str, n_clicks=0),
    # drop down menu to select cluster
    dcc.Dropdown(
        id="filter_dropdown" + id_str,
        # options=[{"label": i[1], "value": i[0]} for i in set_cluster],
        placeholder="-Select a Cluster-",
        multi=False,
        # value=list([i[0] for i in set_cluster])
    ),

    # data table to display the cluster
    dash_table.DataTable(
        id='manual',
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
    html.Button('Choose random sequence', id='random' + qid_str, n_clicks=0),
    html.H3(id='doneCluster' + qid_str),
    html.Button('Submit change', id='submit' + qid_str, n_clicks=0),
    html.H3(id="successful" + qid_str),

    ## Selected sequence context
    # Selected sequence context
    html.Div(className='manual_context', children=[
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
        dcc.Store(id='selected row' + id_str)

    ], ),
    dmc.Modal( title="Yeeeeeeeeaaaaaaaa", id = "modal_set_cluster"+id_str),
    dmc.Modal( title="Noooooooo", id = "modal_set_risk"+id_str),
],
    # dcc.Store stores the intermediate value
    style=style.content_style
)
