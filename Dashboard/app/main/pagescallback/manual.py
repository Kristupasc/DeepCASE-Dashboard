import dash
from dash import html, dash_table, dcc, callback, Output, Input
import pandas as pd
import Dashboard.app.main.recources.loaddata as load
import Dashboard.app.main.recources.style as style
id_str = "_ma"
df = load.formatSequenceCluster(0, id_str)
set_cluster = load.possible_clusters()


@callback(
    Output('manual-analysis', "data"),
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