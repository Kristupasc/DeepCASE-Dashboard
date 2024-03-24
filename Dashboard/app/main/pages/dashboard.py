import os
import matplotlib.dates as mdates

import dash
import pandas as pd
from dash import html, dcc, callback, dash_table
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import Dashboard.app.main.recources.style as style
from Dashboard.data.dao.dao import DAO

# create csv x2
# upload through database
# make it cluster on dashboard

dash.register_page(__name__, path="/", name="Dashboard", title="Dashboard", order=0)
import dash
from dash import html, dash_table, dcc, callback, Output, Input
import pandas as pd
import Dashboard.app.main.recources.loaddata as load
import Dashboard.app.main.recources.style as style
from Dashboard.app.main.pagescallback.dashboard import *

def choose_risk(weight):
    # A weight can be between 0 and 100. The higher the weight, the higher the risk
    if weight == 0:
        return "Unlabeled"
    elif weight < 1:
        return "Info"
    elif weight < 3:
        return "Low"
    elif weight < 5:
        return "Medium"
    elif weight < 7:
        return "High"
    elif weight < 9:
        return "Suspicious"
    else:
        return "Attack"

# Define color scheme
colors = {
    "background": "#FFFFFF",  # white background
    "text": "#000000",  # black text for visibility
    "Risk Label": {
        "Info": "#45B6FE",  # blue
        "Low": "#FFD700",  # gold
        "Medium": "#FF8C00",  # darkorange
        "High": "#FF4500",  # orangered
        "Attack": "#DC143C",  # crimson
        "Suspicious": "#800080",  # purple
        "Unlabeled": "#808080"  # grey
    }
}

########################################################################
#   Dash objects page(Makes use of the callback addition)    #
########################################################################

layout = html.Div([
    html.H1('Dash'),
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
        id='dashboard',
        columns=[
            {'name': 'Date', 'id': 'timestamp' + id_str, 'type': 'text'},
            {'name': 'Source', 'id': 'machine' + id_str, 'type': 'text'},
            {'name': 'Event', 'id': 'id_cluster'+id_str, 'type': 'numeric', 'hideable': True},
            {'name': 'Event_text', 'id': 'name' + id_str, 'type': 'text', 'hideable': True},
            {'name': 'Risk', 'id': 'risk_label' + id_str, 'type': 'numeric'},
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
            {'name': 'Position(top old, bottom newest)', 'id': 'event_position'+cid_str, 'type': 'numeric', 'hideable': True},
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
    html.Div(
        [
            html.H2("All Clusters", className="graph__title"),
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
dcc.Store(id='selected row'+ id_str)

],
    # dcc.Store stores the intermediate value
    style=style.content_style)


@callback(
    Output("scatter-plot", "figure"),
    [Input("filter_dropdown"+ id_str, "value")]
)
def generate_scatter_plot(selected_cluster):
    print(selected_cluster)
    traces = []
    dao = DAO()
    x = []
    y = []
    colors_graph = []
    # check if selected_cluster is a list
    if not isinstance(selected_cluster, list):
        data = dao.get_sequences_per_cluster(selected_cluster)
        for sequence in data.to_dict('records'):
            timestamp = sequence["timestamp"]
            # convert the unix timestamp to date
            timestamp = pd.to_datetime(timestamp, unit='s')
            risk_label = sequence["risk_label"]
            x.append(timestamp)
            y.append(risk_label)
            colors_graph.append(colors["Risk Label"][choose_risk(int(risk_label))])
    traces.append(
        go.Scatter(
            x=x,
            y=y,
            mode='markers',
            opacity=0.7,
            marker={
                'size': 15,
                'line': {'width': 0.5, 'color': 'white'},
                'color': colors_graph,
            },
            name="Sda"
        )
    )

    return {
        "data": traces,
        "layout": go.Layout(
            xaxis={"title": "Timeline"},
            yaxis={"title": "Security score"},
            margin={"l": 40, "b": 40, "t": 10, "r": 10},
            legend={"x": 0, "y": 1},
            hovermode="closest",
            transition={"duration": 500},
            plot_bgcolor=colors["background"],
            paper_bgcolor=colors["background"],
            font={"color": colors["text"]},
        ),
    }