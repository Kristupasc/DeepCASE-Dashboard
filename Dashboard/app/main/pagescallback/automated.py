import dash
from dash import html, dash_table, dcc, callback, Output, Input
import pandas as pd
import Dashboard.app.main.recources.loaddata as load
id_str = "_sa"
cid_str = "_cisa"
df = load.formatSequenceCluster(0, id_str)
set_cluster = load.possible_clusters()
@callback(
    Output("semi-automatic", "data"),
    Input("filter_dropdown"+id_str, "value")
)
def display_table(state):
    global df
    if isinstance(state, int):
        dff = load.formatSequenceCluster(state, id_str)
        df = dff
        return dff.to_dict("records")
    else:
        return df.to_dict("records")

