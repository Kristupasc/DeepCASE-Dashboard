from dash import callback, Output, Input
from dash.exceptions import PreventUpdate

import Dashboard.app.main.pagescallback.display_sequence as display_sequence
import Dashboard.app.main.recources.loaddata as load

########################################################################
#   Semi-automatic callback (All ids need to match 100%)               #
########################################################################
# suffix for all the ids that might be the same.
id_str = "_sa"
cid_str = "_cisa"
# Setting variables
cluster = 0

callback(
    Output('selected cluster' + id_str, "data"),
    Input("filter_dropdown" + id_str, "value")
)(display_sequence.store_selected_cluster)


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


callback(
    Output('selected row' + id_str, "data"),
    Input("semi-automatic", 'selected_rows'),
    Input("selected cluster" + id_str, "data")
)(display_sequence.store_context_row)


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


callback(
    Output("filter_dropdown" + id_str, 'options'),
    Input('url', 'pathname')
)(display_sequence.update_options_dropdown)

callback(
    Output("filter_dropdown" + id_str, 'value'),
    Input('url', 'pathname')
)(display_sequence.update_values_dropdown)

callback(
    Output('cluster name' + id_str, 'children'),
    Input('selected cluster' + id_str, "data")
)(display_sequence.get_name_cluster)
########################################################################################
# Light up the selected row.
########################################################################################
callback(
    Output("semi-automatic", "style_data_conditional"),
    Input("selected row" + id_str, "data")
)(display_sequence.light_up_selected_row)