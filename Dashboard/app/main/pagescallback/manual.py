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
cluster = 0
df = load.formatSequenceCluster(0, id_str)
set_cluster = load.possible_clusters()
@callback(
    Output('selected cluster' + id_str, "data"),
    Input("filter_dropdown"+id_str, "value")
)
def store_selected_cluster(state):
    if isinstance(state, int):
        return state
    raise PreventUpdate
@callback(
    Output("manual", "data"),
    Input('selected cluster' + id_str, "data")
)
def update_table_cluster(state):
    if isinstance(state, int):
        dff = load.formatSequenceCluster(state, id_str)
        return dff.to_dict("records")
    raise PreventUpdate

@callback(
    Output('selected row' + id_str, "data"),
    Input("manual", 'selected_rows')
)
def store_context_row(state):
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
    Input('change cluster name'+id_str, 'n_clicks')
)
def update_options_dropdown(n):
    if 'change cluster name' + id_str == ctx.triggered_id:
        return [{"label": i[1], "value": i[0]} for i in load.possible_clusters()]
    return [{"label": i[1], "value": i[0]} for i in load.possible_clusters()]
@callback(
    Output("filter_dropdown"+ id_str, 'value'),
    Input('change cluster name'+id_str, 'n_clicks')
)
def update_values_dropdown(n):
    if 'change cluster name'+id_str == ctx.triggered_id:
        return list([i[0] for i in load.possible_clusters()])
    return list([i[0] for i in load.possible_clusters()])
@callback(
    Output('cluster name' + id_str, 'value'),
    Input('selected cluster' + id_str,"data")
)
def get_name_cluster(data):
    if isinstance(data, int):
        k =  load.possible_clusters()
        for z in k:
            if z[0] == data:
                return z[1]
    return "Cluster not selected"

########################################################################################
# Editable callback extra functionality special for manual.
########################################################################################

@callback(
    Output("set label cluster"+id_str, 'children'),
    Input('selected cluster' + id_str, "data"),
    Input('change cluster name'+id_str, 'n_clicks'),
    State('cluster name'+id_str, 'value')
)
def set_cluster_name(cluster_id, n_clicks, value):
    if 'change cluster name'+id_str == ctx.triggered_id:
        if isinstance(cluster_id, int) and isinstance(value, str):
            if load.set_cluster_name(cluster_id, value):
                return "Successful changed"
    return "cluster name unchanged"

@callback(
    Output("successful"+qid_str, "children"),
    Input('risk_label'+qid_str, "value"),
    Input('selected row' + id_str,"data"),
    Input('selected cluster' + id_str, "data"),
    Input('submit' + qid_str, "n_clicks")
)
def set_risk_label(value, row, cluster, n_clicks):
    if 'submit' + qid_str == ctx.triggered_id:
        if isinstance(row, int) and isinstance(cluster, int) and isinstance(value, int):
            if load.set_riskvalue(cluster_id=cluster,row =row , risk_value=value):
                return "Successful, saved."
    return "Nothing saved"

@callback(
    Output("chosen sequence manual", "data"),
    Input('selected row' + id_str,"data"),
    Input('selected cluster' + id_str, "data"),
)
def display_judged_sequence( row, cluster):
    if isinstance(row, int) and isinstance(cluster, int):
      return load.selectEventFormatted(cluster, row, qid_str).to_dict('records')
    return pd.DataFrame().to_dict('records')