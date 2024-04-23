from dash import callback, Output, Input
from dash.exceptions import PreventUpdate

# Importing callback functions and data loading functions
import Dashboard.app.main.pagescallback.common as display_sequence
import Dashboard.app.main.recources.loaddata as load

# Setting suffixes for IDs
id_str = "_sa"  # suffix for semi-automatic IDs
cid_str = "_cisa"  # suffix for context information IDs

# Callback to store the selected cluster
callback(
    Output('selected cluster' + id_str, "data"),  # Output: selected cluster data
    Input("filter_dropdown" + id_str, "value")  # Input: value of filter dropdown
)(display_sequence.store_selected_cluster)


# Callback to update the table based on the selected cluster
@callback(
    Output("semi-automatic", "data"),  # Output: data for semi-automatic table
    Input('selected cluster' + id_str, "data")  # Input: selected cluster data
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


# Callback to store the selected row
callback(
    Output('selected row' + id_str, "data"),  # Output: selected row data
    Input("semi-automatic", 'selected_rows'),  # Input: selected rows in semi-automatic table
    Input("selected cluster" + id_str, "data")  # Input: selected cluster data
)(display_sequence.store_context_row)


# Callback to display context information based on the selected row and cluster
@callback(
    Output('Context information' + cid_str, "data"),  # Output: context information data
    Input('selected row' + id_str, "data"),  # Input: selected row data
    Input('selected cluster' + id_str, "data")  # Input: selected cluster data
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


# Callbacks for updating dropdown options and values
callback(
    Output("filter_dropdown" + id_str, 'options'),  # Output: options for filter dropdown
    Input('refresh-data-automatic', 'n_intervals')  # Input: number of intervals for refresh
)(display_sequence.update_options_dropdown)

callback(
    Output("filter_dropdown" + id_str, 'value'),  # Output: value for filter dropdown
    Input('url', 'pathname')  # Input: pathname from URL
)(display_sequence.update_values_dropdown)

# Callback to get the name of the selected cluster
callback(
    Output('cluster name' + id_str, 'children'),  # Output: children of cluster name component
    Input('selected cluster' + id_str, "data")  # Input: selected cluster data
)(display_sequence.get_name_cluster)

# Callback to light up the selected row
callback(
    Output("semi-automatic", "style_data_conditional"),  # Output: style_data_conditional for semi-automatic table
    Input("selected row" + id_str, "data")  # Input: selected row data
)(display_sequence.light_up_selected_row)

# Callback to find the risk value of cluster and display
callback(
    Output("display risk cluster" + id_str, "children"),  # Output: children of display risk cluster component
    Input('selected cluster' + id_str, "data")  # Input: selected cluster data
)(display_sequence.display_risk_cluster)
