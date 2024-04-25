import pandas as pd

from Dashboard.data.dao.dao import DAO


def get_colors():
    """
        Get the color palette used for visualization.

        Returns
        -------
        dict
            A dictionary containing color codes for different components.
        """
    return {
        "background": "rgba(132, 213, 230, 0)",  # white background
        "text": "#ffab40",
        "Risk Label": {
            "Info": "#45B6FE",  # blue
            "Low": "#FFD700",  # gold
            "Medium": "#FF8C00",  # darkorange
            "High": "#FF4500",  # orangered
            "Attack": "#DC143C",  # crimson
            "Suspicious": "#800080",  # purple
            "Unlabeled": "#808080",  # grey
            "Custom": "#808080"  # grey
        }
    }


def choose_risk(weight):
    """
    Choose the risk label based on the weight.

    Parameters
    ----------
    weight : int
        The weight value representing the risk.

    Returns
    -------
    str
        The risk label.
    """
    # TODO: change it to accept a different format than 0-10
    if weight <= 0:
        return "Unlabeled"
    elif weight <= 1:
        return "Info"
    elif weight <= 3:
        return "Low"
    elif weight <= 5:
        return "Medium"
    elif weight <= 7:
        return "High"
    else:
        return "Attack"


def get_risk_cluster(cluster_id):
    """
    Get the maximum risk label for a cluster.

    Parameters
    ----------
    cluster_id : int
        Cluster ID.

    Returns
    -------
    int
        Maximum risk label.
    """
    dao = DAO()
    df = dao.get_sequences_per_cluster(cluster_id).reindex()
    df['risk_label'] = pd.to_numeric(df['risk_label'])
    return df['risk_label'].max()


def function_risk(cluster_id) -> str:
    """
    Helper function, to get risk value.

    Parameters
    ----------
    cluster_id : int
        The id of the cluster, where to get the risk value.

    Returns
    -------
    str
        Representing the risk label.
    """
    return choose_risk(get_risk_cluster(cluster_id))
