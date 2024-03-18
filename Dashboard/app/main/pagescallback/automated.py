import dash
from dash import html, dash_table, dcc, callback, Output, Input
import pandas as pd
from dash.exceptions import PreventUpdate

import Dashboard.app.main.recources.loaddata as load
id_str = "_sa"
cid_str = "_cisa"
cluster = 0
df = load.formatSequenceCluster(0, id_str)
set_cluster = load.possible_clusters()
@callback(
    Output('selected row' + id_str, "data"),
    Input("filter_dropdown"+id_str, "value")
)
def display_table_cluster(state):
    if isinstance(state, int):
        dff = load.formatSequenceCluster(state, id_str)
        return dff.to_json(date_format='iso', orient='split')
    raise PreventUpdate
@callback(
    Output("semi-automatic", "data"),
    Input('selected row' + id_str, "data")
)
def update_table_cluster(state):
    if isinstance(state, int):
        dff = pd.read_json(state, orient='split')
        return dff.to_dict("records")
    raise PreventUpdate


# @callback(
#     Output('Context information'+cid_str, "data"),
#     Input("semi-automatic", 'selected_rows')
# )
# def display_table_context(selected_rows):
#     pass
#     print(selected_rows)
#
#     print('column-{}')
#     return PreventUpdate