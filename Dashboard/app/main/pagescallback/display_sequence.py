import pandas as pd
from Dashboard.app.main.recources.label_tools import choose_risk
import Dashboard.app.main.recources.loaddata as load


# Function to store the selected cluster
def store_selected_cluster(state):
    """
    Store the selected cluster

    :param state: the selected value from the filter dropdown
    :return: the selected cluster
    """
    if isinstance(state, int):
        return state
    return None


# Function to store the selected row for context
def store_context_row(state, cluster):
    """
    Store the selected row for context.

    :param state: the selected rows from the dashboard
    :param cluster: the cluster id, and a way to trigger this methode. To prevent an outbound.
    :return: the selected row if it's an integer
    """
    if state is not None:
        if len(state) > 0 and isinstance(cluster, int):
            if isinstance(state[0], int):
                return min(state[0], load.get_row(cluster) - 1)
    return None


# Function to update the options in the dropdown
def update_options_dropdown(n):
    """
    Update the options in the dropdown.

    :return: a list of options for the dropdown based on possible clusters with labels and values
    """
    if n is None:
        return [{"label": i[1], "value": i[0]} for i in load.possible_clusters() if
                not pd.isna(i[1]) and not pd.isna(i[0])]
    return [{"label": i[1], "value": i[0]} for i in load.possible_clusters() if not pd.isna(i[1]) and not pd.isna(i[0])]


# Function to update the values in the dropdown
def update_values_dropdown(n):
    """
    Update the values in the dropdown.
    :return: a list of values for the dropdown based on possible clusters
    """
    if n is None:
        return list([i[0] for i in load.possible_clusters() if not pd.isna(i[0])])
    return list([i[0] for i in load.possible_clusters() if not pd.isna(i[0])])


# Function to get the name of the selected cluster
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
                return str(z[1])  # Don't change this this will create an easy infinity loop.
    return "Cluster not selected"


# Function to light up the selected row
def light_up_selected_row(row):
    """
    Light up the selected event.
    :param row: the row selected
    :return: the adjusted layout
    """
    if isinstance(row, int):
        return [{"if": {"row_index": row % 10}, 'backgroundColor': 'hotpink',
                 'color': 'orange', }]
    return None


# Function to display the risk value of the cluster
def display_risk_cluster(cluster_id):
    try:
        return "Security Score: ", choose_risk(load.get_risk_cluster(cluster_id))
    except (ValueError, IndexError):
        return ""
