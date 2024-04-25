import random

from Dashboard.app.main.recources.get_tables import get_cluster_table
from Dashboard.app.main.recources.label_tools import function_risk
from Dashboard.data.dao.dao import DAO


def get_algorithm_sequence(cluster_id):
    """
    Returns a list of row numbers where the value in column 'risk_label' is negative
    or where there is a unique combination['machine', 'risk_label', 'id_event'] of other specified columns.
    From the list a random element is selected.

    Parameters
    ----------
    cluster_id : int
        Cluster ID to determine which cluster to be used.

    Returns
    -------
    int
        Number in the list of row numbers that meet the conditions.
    """
    dataframe = get_cluster_table(cluster_id, "")
    filtered_rows = []
    negative_rows = dataframe.index[dataframe["risk_label"] < 0].tolist()
    filtered_rows.extend(negative_rows)
    unique_rows = dataframe.drop_duplicates(subset=['machine', 'risk_label', 'id_event']).index.tolist()
    filtered_rows.extend(unique_rows)
    the_list = list(set(filtered_rows))
    try:
        rand = random.choice(the_list)
        return rand
    except (ValueError, IndexError):
        return None


def get_algorithm_cluster():
    """
    Returns a random cluster_id that is selected as priority.

    Returns
    -------
    int
        Random cluster ID.
    """
    dao = DAO()
    df = dao.get_clusters_result()
    df["risk"] = df["id_cluster"].apply(function_risk)
    filter_name = ["Attack", "High", "Unlabeled"]
    filtered_rows = df[df['risk'].isin(filter_name)]
    cluster_ids = filtered_rows['id_cluster'].tolist()
    the_list = list(set(cluster_ids))
    try:
        rand = random.choice(the_list)
        return rand
    except (ValueError, IndexError):
        return None


def get_random_cluster():
    """
    Get a random cluster.

    Returns
    -------
    int
        Random cluster ID.
    """
    dao = DAO()
    df = dao.get_clusters_result()
    rows = df.shape[0]
    try:
        rand = random.randrange(0, rows, 1)
        return df.iloc[rand].at["id_cluster"]
    except (ValueError, IndexError):
        return None


def get_random_sequence(cluster_id):
    """
    Get a random sequence.

    Parameters
    ----------
    cluster_id : int
        Cluster ID.

    Returns
    -------
    int
        Random sequence index.
    """
    dao = DAO()
    df = dao.get_sequences_per_cluster(cluster_id)
    rows = df.shape[0]
    rand = random.randrange(0, rows, 1)
    return rand


def get_row(cluster_id):
    """
    Get the max row number.

    Parameters
    ----------
    cluster_id : int
        Cluster ID.

    Returns
    -------
    int
        Random sequence index.
    """
    dao = DAO()
    df = dao.get_sequences_per_cluster(cluster_id)
    rows = df.shape[0]
    return rows
