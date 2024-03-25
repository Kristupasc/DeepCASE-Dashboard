from io import StringIO

import dash
from dash import html, dash_table, dcc, callback, Output, Input
import pandas as pd
from dash.exceptions import PreventUpdate

import Dashboard.app.main.recources.loaddata as load
########################################################################
#   Dashboard callback (All ids need to match 100%)               #
########################################################################
#suffix for all the ids that might be the same.
id_str = "_da"
cid_str = "_cida"
cluster = 0
df = load.formatSequenceCluster(0, id_str)
set_cluster = load.possible_clusters()
@callback(
    Output('selected cluster' + id_str, "data"),
    Input("filter_dropdown"+id_str, "value")
)
def store_selected_cluster(state):
    """
    This methode stores the variable of the dropdown menu.
    Parameters
    ----------
    state: The variable that contains the value.

    Returns
    -------
    Return: either PreventUpdate signal
    or the state to store.

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
    This methode returns a data frame for the cluster table
    Parameters
    ----------
    state is the value that is stored from the selected
    state.

    Returns
    -------
    The dataframe necessary for the cluster.

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
    This methode stores the selected row.
    Parameters
    ----------
    :parameter: state which row is selected.

    Returns
    -------
    The value that needs to be stored.

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
    This makes the context visible
    :param row: the row that is selected
    :param cluster: the cluster that is selected
    :return: the context frame.
    """
    if isinstance(row, int) and isinstance(cluster, int):
        df = load.formatContext(cluster, row, cid_str)
        return df.to_dict("records")
    raise PreventUpdate

@callback(
    Output("filter_dropdown"+ id_str, 'options'),
    Input('interval'+ id_str, 'n_intervals')
)
def update_options_dropdown(n):
    return [{"label": i[1], "value": i[0]} for i in load.possible_clusters()]
@callback(
    Output("filter_dropdown"+ id_str, 'value'),
    Input('interval'+ id_str, 'n_intervals')
)
def update_values_dropdown(n):
    return list([i[0] for i in load.possible_clusters()])
@callback(
    Output('cluster name' + id_str, 'children'),
    Input('selected cluster' + id_str,"data")
)
def get_name_cluster(data):
    if isinstance(data, int):
        k =  load.possible_clusters()
        for z in k:
            if z[0] == data:
                return z[1]
