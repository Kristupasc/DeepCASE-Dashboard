import Dashboard.app.main.recources.style as style
from Dashboard.app.main.pagescallback.dashboard import *


dash.register_page(__name__, path="/", name="Dashboard", title="Dashboard", order=0)

########################################################################
#   Dash objects page(Makes use of the callback addition)    #
########################################################################

layout = html.Div([
    html.H1('Dash'),
    html.H2('cluster name unknown', id='cluster name' + id_str),
    # drop down menu to select cluster
    dcc.Dropdown(
            id="filter_dropdown"+ id_str,
            options=update_options_dropdown(),
            value=update_values_dropdown(),
            placeholder="-Select a Cluster-",
            multi=False,
        ),

    # data table to display the cluster
    dash_table.DataTable(
        id='dashboard',
        columns=[
            {'name': 'Date', 'id': 'timestamp' + id_str, 'type': 'text'},
            {'name': 'Source', 'id': 'machine' + id_str, 'type': 'text'},
            {'name': 'Event', 'id': 'id_event'+id_str, 'type': 'numeric', 'hideable': True},
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
    html.H2('Context of the selected sequence', id='sequence name' + cid_str),
    # Table to show the context of a sequence
    dash_table.DataTable(
        id='Context information'+cid_str,
        columns=[
            {'name': 'Position(top old, bottom newest)', 'id': 'event_position'+cid_str, 'type': 'numeric', 'hideable': True},
            {'name': 'event', 'id': 'event'+cid_str, 'type': 'text', 'hideable': True},
            {'name': 'Event_name', 'id': 'name'+cid_str, 'type': 'text', 'hideable': True},
            {'name': 'Attention', 'id': 'attention'+cid_str, 'type': 'text'}
        ],
        # data=df.to_dict('records'),
        filter_action='native',

        style_data={
            'width': 'normal', 'minWidth': 'normal', 'maxWidth': 'normal',
            'overflow': 'hidden',
            'textOverflow': 'ellipsis',
        },
        page_size=10),
    html.Div(
        [
            html.H2("All Sequences in Cluster", className="graph__title"),
            dcc.Graph(id="scatter-plot"),
            dcc.Interval(
                id="scatter-update",
                interval=int(5000),
                n_intervals=0,
            ),
        ],
        className="graph",
    ),
    # Objects to store intermediate values, selected by the above table.
dcc.Store(id='selected cluster'+ id_str),
dcc.Store(id='selected row'+ id_str),

],
    # dcc.Store stores the intermediate value
    style=style.content_style)
