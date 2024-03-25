from io import StringIO

import dash
from dash import html, dash_table, dcc, callback, Output, Input,ctx
import pandas as pd
from dash.exceptions import PreventUpdate
import plotly.graph_objs as go
import Dashboard.app.main.recources.loaddata as load
from Dashboard.app.main.recources.label_tools import choose_risk, get_colors
from Dashboard.data.dao.dao import DAO

########################################################################
#   Dashboard callback (All ids need to match 100%)               #
########################################################################
#suffix for all the ids that might be the same.
id_str = "_da"
cid_str = "_cida"
#Setting variables
cluster = 0
df = load.formatSequenceCluster(0, id_str)
set_cluster = load.possible_clusters()
@callback(
    Output('selected cluster' + id_str, "data"),
    Input("filter_dropdown"+id_str, "value")
)
def store_selected_cluster(state):
    """
      Store the selected cluster.

      :param state: the selected value from the filter dropdown
      :return: the selected cluster if it's an integer
      """
    if isinstance(state, int):
        return state
    raise PreventUpdate
@callback(
    Output("dashboard", "data"),
    Input('selected cluster' + id_str, "data")
)
def update_table_cluster(state):
    """
    Update the dashboard table based on the selected cluster.

    :param state: the selected cluster
    :return: the updated table data if the cluster is an integer
    """
    if isinstance(state, int):
        dff = load.formatSequenceCluster(state, id_str)
        return dff.to_dict("records")
    raise PreventUpdate

@callback(
    Output('selected row' + id_str, "data"),
    Input("dashboard", 'selected_rows')
)
def store_context_row(state):
    """
    Store the selected row for context.

    :param state: the selected rows from the dashboard
    :return: the selected row if it's an integer
    """
    if state is not None:
        if len(state)>0:
            if isinstance(state[0], int):
                return state[0]
    raise PreventUpdate
@callback(
    Output('Context information' + cid_str, "data"),
    Input('selected row' + id_str, "data"),
    Input('selected cluster' + id_str, "data")
)
def display_context(row, cluster):
    """
    Display the context information based on the selected row and cluster.

    :param row: the selected row
    :param cluster: the selected cluster
    :return: the context frame as a dictionary of records
    """
    if isinstance(row, int) and isinstance(cluster, int):
        df = load.formatContext(cluster, row, cid_str)
        return df.to_dict("records")
    raise PreventUpdate

@callback(
    Output("filter_dropdown" + id_str, 'options'),
    Input('change cluster name', 'n_clicks')
)
def update_options_dropdown(n):
    """
    Update the options in the dropdown based on the change cluster name button click.

    :param n: the number of clicks on the change cluster name button
    :return: a list of options for the dropdown based on possible clusters with labels and values
    """
    if 'change cluster name' == ctx.triggered_id:
        return [{"label": i[1], "value": i[0]} for i in load.possible_clusters()]
    return [{"label": i[1], "value": i[0]} for i in load.possible_clusters()]
@callback(
    Output("filter_dropdown" + id_str, 'value'),
    Input('change cluster name', 'n_clicks')
)
def update_values_dropdown(n):
    """
    Update the values in the dropdown based on the change cluster name button click.

    :param n: the number of clicks on the change cluster name button
    :return: a list of values for the dropdown based on possible clusters
    """
    if 'change cluster name' == ctx.triggered_id:
        return list([i[0] for i in load.possible_clusters()])
    return list([i[0] for i in load.possible_clusters()])
@callback(
    Output('cluster name' + id_str, 'children'),
    Input('selected cluster' + id_str, "data")
)
def get_name_cluster(data):
    """
    Get the name of the selected cluster based on the cluster ID.

    :param data: the selected cluster ID
    :return: the name of the selected cluster or a default message if no cluster is selected
    """
    if isinstance(data, int):
        k = load.possible_clusters()
        for z in k:
            if z[0] == data:
                return z[1]
    return "Cluster not selected"

@callback(
    Output("scatter-plot", "figure"),
    [Input("filter_dropdown" + id_str, "value")]
)
def generate_scatter_plot(selected_cluster):
    """
    Generate a scatter plot based on the selected cluster.

    :param selected_cluster: the value selected in the filter dropdown
    :return: a dictionary containing the data and layout for the scatter plot
    """
    # print(selected_cluster)
    traces = []
    dao = DAO()
    x = []
    y = []
    colors_graph = []
    colors = get_colors()
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