from io import StringIO

import dash
from dash import html, dash_table, dcc, callback, Output, Input,ctx, State
import pandas as pd
from dash.exceptions import PreventUpdate

import Dashboard.app.main.recources.loaddata as load
########################################################################
#   Manual callback (All ids need to match 100%)               #
########################################################################
#suffix for all the ids that might be the same.
id_str = "_ma"
cid_str = "_cma"
qid_str = "-qma"
# Some initial values
cluster = 0
# df = load.formatSequenceCluster(0, id_str)
# set_cluster = load.possible_clusters()
@callback(
    Output('selected cluster' + id_str, "data"),
    Input("filter_dropdown" + id_str, "value"),
    Input('random' + id_str, "n_clicks")
)
def store_selected_cluster(state, click):
    """
    Store the selected cluster based on dropdown value or random click.

    :param state: the value from the filter dropdown
    :param click: the number of clicks on the random button
    :return: the selected cluster or trigger a PreventUpdate exception
    """
    if 'random' + id_str == ctx.triggered_id:
        return load.get_random_cluster()
    if isinstance(state, int):
        return state
    raise PreventUpdate

@callback(
    Output("manual", "data"),
    Input('selected cluster' + id_str, "data")
)
def update_table_cluster(state):
    """
    Update the table in the manual component based on the selected cluster.

    :param state: the selected cluster ID
    :return: the formatted data for the table as a dictionary of records
    """
    if isinstance(state, int):
        dff = load.formatSequenceCluster(state, id_str)
        return dff.to_dict("records")
    raise PreventUpdate
@callback(
    Output('selected row' + id_str, "data"),
    Input("manual", 'selected_rows'),
    Input('random' + qid_str, "n_clicks"),
    Input("selected cluster" + id_str, "data")
)
def store_context_row(state, click, cluster_id):
    """
    Store the context row based on user interactions and trigger events.

    :param state: the selected rows in the manual component
    :param click: the number of clicks on the random button
    :param cluster_id: the selected cluster ID
    :return: the stored context row or trigger a PreventUpdate exception
    """
    if 'random' + qid_str == ctx.triggered_id:
        return load.get_random_sequence(cluster_id)
    if state is not None:
        if len(state) > 0:
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
    This function displays the context information based on the selected row and cluster.

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
    Output('cluster name' + id_str, 'value'),
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

########################################################################################
# Editable callback extra functionality special for manual.
########################################################################################

@callback(
    Output("set label cluster" + id_str, 'children'),
    Input('selected cluster' + id_str, "data"),
    Input('change cluster name', 'n_clicks'),
    State('cluster name' + id_str, 'value')
)
def set_cluster_name(cluster_id, n_clicks, value):
    """
    Set the label for the cluster based on user input.

    :param cluster_id: the selected cluster ID
    :param n_clicks: the number of clicks on the change cluster name button
    :param value: the new value for the cluster name
    :return: a message indicating the success of the operation or unchanged status
    """
    if 'change cluster name' == ctx.triggered_id:
        if isinstance(cluster_id, int) and isinstance(value, str):
            if load.set_cluster_name(cluster_id, value):
                return "Successful changed"
    return "cluster name unchanged"


@callback(
    Output("successful" + qid_str, "children"),
    Input('risk_label' + qid_str, "value"),
    Input('selected row' + id_str, "data"),
    Input('selected cluster' + id_str, "data"),
    Input('submit' + qid_str, "n_clicks")
)
def set_risk_label(value, row, cluster, n_clicks):
    """
    Set the risk label based on user input.

    :param value: the risk label value
    :param row: the selected row
    :param cluster: the selected cluster
    :param n_clicks: the number of clicks on the submit button
    :return: a message indicating the success of the operation
    """
    if 'submit' + qid_str == ctx.triggered_id:
        if isinstance(row, int) and isinstance(cluster, int) and isinstance(value, int):
            if load.set_riskvalue(cluster_id=cluster, row=row, risk_value=value):
                return "Successful, saved."
    return "Nothing saved"

@callback(
    Output("chosen sequence manual", "data"),
    Input('selected row' + id_str, "data"),
    Input('selected cluster' + id_str, "data"),
)
def display_judged_sequence(row, cluster):
    """
    Display the judged sequence based on the selected row and cluster.

    :param row: the selected row
    :param cluster: the selected cluster
    :return: the judged sequence as a dictionary of records
    """
    if isinstance(row, int) and isinstance(cluster, int):
      return load.selectEventFormatted(cluster, row, qid_str).to_dict('records')
    return pd.DataFrame().to_dict('records')