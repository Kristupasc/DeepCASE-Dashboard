import pandas as pd
from dash.exceptions import PreventUpdate

from Dashboard.app.main.recources.label_tools import choose_risk
import Dashboard.app.main.recources.loaddata as load
from Dashboard.data.dao.dao import DAO

# Function to store the selected cluster
def store_selected_cluster(state):
    """
    Store the selected cluster.

    Parameters
    ----------
    state :
        The selected value from the filter dropdown

    Returns
    -------
    int or None
        The selected cluster or None if state is not an integer
    """
    if isinstance(state, int):
        return state
    return None


# Function to store the selected row for context
def store_context_row(state, cluster):
    """
    Store the selected row for context.

    Parameters
    ----------
    state :
        The selected rows from the dashboard
    cluster :
        The cluster id, and a way to trigger this method. To prevent an outbound.

    Returns
    -------
    int or None
        The selected row if it's an integer, else None
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

    Parameters
    ----------
    n :
        A dummy parameter to ensure callback execution

    Returns
    -------
    list of dict
        A list of options for the dropdown based on possible clusters with labels and values
    """
    if n is None:
        return [{"label": i[1], "value": i[0]} for i in load.possible_clusters() if
                not pd.isna(i[1]) and not pd.isna(i[0])]
    return [{"label": i[1], "value": i[0]} for i in load.possible_clusters() if not pd.isna(i[1]) and not pd.isna(i[0])]


# Function to update the values in the dropdown
def update_values_dropdown(n):
    """
    Update the values in the dropdown.

    Parameters
    ----------
    n :
        A dummy parameter to ensure callback execution

    Returns
    -------
    list
        A list of values for the dropdown based on possible clusters
    """
    if n is None:
        return list([i[0] for i in load.possible_clusters() if not pd.isna(i[0])])
    return list([i[0] for i in load.possible_clusters() if not pd.isna(i[0])])


# Function to get the name of the selected cluster
def get_name_cluster(data):
    """
    Get the name of the selected cluster based on the cluster ID.

    Parameters
    ----------
    data :
        The selected cluster ID

    Returns
    -------
    str
        The name of the selected cluster or a default message if no cluster is selected
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

    Parameters
    ----------
    row :
        The row selected

    Returns
    -------
    list of dict or None
        The adjusted layout or None if row is not an integer
    """
    if isinstance(row, int):
        return [{"if": {"row_index": row % 10}, 'backgroundColor': 'hotpink',
                 'color': 'orange', }]
    return None


# Function to display the risk value of the cluster
def display_risk_cluster(cluster_id):
    """
    Display the risk value of the cluster.

    Parameters
    ----------
    cluster_id :
        The ID of the selected cluster

    Returns
    -------
    str
        The risk label of the cluster or an empty string if cluster_id is None or not an integer
    """
    if cluster_id is None or not isinstance(cluster_id, int):
        return ""
    dao = DAO()
    data = dao.get_sequences_per_cluster(cluster_id)
    # if the cluster was just selected, we check for the label of the cluster
    # set the risk label to the first sequence in the cluster
    cluster_risk_label = "Security Score: " + str(choose_risk(data.iloc[0]["risk_label"]))
    # iterate through the sequences and check if all have the same label
    for sequence in data.to_dict('records'):
        if sequence["risk_label"] != data.iloc[0]["risk_label"]:
            cluster_risk_label = "Security Score: Suspicious"
            break
    return cluster_risk_label