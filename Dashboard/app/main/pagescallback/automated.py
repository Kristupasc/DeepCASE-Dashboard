from io import StringIO

import dash
from dash import html, dash_table, dcc, callback, Output, Input,ctx
import pandas as pd
from dash.exceptions import PreventUpdate

import Dashboard.app.main.recources.loaddata as load
########################################################################
#   Semi-automatic callback (All ids need to match 100%)               #
########################################################################
#suffix for all the ids that might be the same.
id_str = "_sa"
cid_str = "_cisa"
# Setting variables
cluster = 0
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
    Output("semi-automatic", "data"),
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
    Input("semi-automatic", 'selected_rows')
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
    Output('Context information'+cid_str, "data"),
    Input('selected row' + id_str, "data"),
    Input('selected cluster' + id_str,"data")
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
    Input('url', 'pathname')
)
def update_options_dropdown(n):
    """
    Update the options in the dropdown.

    :return: a list of options for the dropdown based on possible clusters with labels and values
    """
    if n is None:
        return  [{"label": i[1], "value": i[0]} for i in load.possible_clusters() if not pd.isna(i[1]) and not pd.isna(i[0])]
    return [{"label": i[1], "value": i[0]} for i in load.possible_clusters() if not pd.isna(i[1]) and not pd.isna(i[0])]
@callback(
    Output("filter_dropdown" + id_str, 'value'),
    Input('url', 'pathname')
)
def update_values_dropdown(n):
    """
    Update the values in the dropdown.
    :return: a list of values for the dropdown based on possible clusters
    """
    if n is None:
        return list([i[0] for i in load.possible_clusters() if not pd.isna(i[0])])
    return list([i[0] for i in load.possible_clusters() if not pd.isna(i[0])])

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
            if not pd.isna(z[0]) and z[0] == float(data):
                return z[1]
    return "Cluster not selected"
