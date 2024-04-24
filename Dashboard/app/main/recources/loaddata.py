import random
import pandas as pd
from Dashboard.app.main.recources.label_tools import choose_risk
from Dashboard.data.dao.dao import DAO
from Dashboard.app.main.recources.run_deepcase import *
format_time = "%H:%M:%S.%f, %d %b %Y"  # For second %s %ssss


def formatSequenceCluster(cluster: int, id_str: str) -> pd.DataFrame:
    """
    Format the sequence cluster DataFrame.

    Parameters
    ----------
    cluster : int
        The cluster ID.
    id_str : str
        ID string to uniquely identify the table.

    Returns
    -------
    pd.DataFrame
        Formatted DataFrame.
    """
    dao = DAO()
    df = dao.get_sequences_per_cluster(cluster_id=cluster)
    df = df[df['id_cluster'] == cluster]
    df = df[['machine', 'timestamp', 'name', 'risk_label', 'id_event']]
    df['timestamp'] = pd.DatetimeIndex(pd.to_datetime(df['timestamp'], unit='s')).strftime(format_time)
    df['risk_label'] = pd.to_numeric(df['risk_label'])
    df['machine'] = pd.Series(df['machine'], dtype="string")
    df['name'] = pd.Series(df['name'], dtype="string")
    df['timestamp'] = pd.Series(df['timestamp'], dtype="string")
    df['id_event'] = pd.Series(df['id_event'], dtype="string")
    dict_id: dict[str, str] = dict()
    for i in df.columns:
        dict_id[i] = i + id_str
    df = df.rename(columns=dict_id)
    return df


def possible_clusters() -> [tuple]:
    """
    Get possible clusters.

    Returns
    -------
    list of tuple
        List of cluster tuples.
    """
    dao = DAO()
    df = dao.get_clusters_result()
    df = df[['id_cluster', 'name_cluster']]
    df['id_cluster'] = pd.Series(df['id_cluster'], dtype="string")
    df['name_cluster'] = pd.Series(df['name_cluster'], dtype="string")
    df['name_cluster'] = df['name_cluster'].fillna(df['id_cluster'])
    df['id_cluster'] = pd.to_numeric(df['id_cluster'])
    df = list(df.itertuples(index=False, name=None))
    return df


def formatContext(cluster: int, index: int, id_str: str) -> pd.DataFrame:
    """
    Format the context DataFrame.

    Parameters
    ----------
    cluster : int
        The cluster ID.
    index : int
        Index of the row.
    id_str : str
        ID string to uniquely identify the table.

    Returns
    -------
    pd.DataFrame
        Formatted DataFrame.
    """
    dao = DAO()
    df = dao.get_sequences_per_cluster(cluster).reindex()
    id_sequence = df.iloc[index].at["id_sequence"]
    df = dao.get_context_per_sequence(int(id_sequence))
    df["event"] = df["name"].apply(get_event_id)
    dict_id: dict[str, str] = dict()
    for i in df.columns:
        dict_id[i] = i + id_str
    df = df.rename(columns=dict_id)
    return df


def get_event_id(event_text):
    """
    Get event ID.

    Parameters
    ----------
    event_text : str
        Event text.

    Returns
    -------
    str
        Event ID.
    """
    dao = DAO()
    df = dao.get_mapping()
    try:
        return df[df["name"] == event_text].iloc[0].at["id"]
    except (ValueError, IndexError):
        return event_text


def set_riskvalue(cluster_id, row, risk_value):
    """
    Set risk value.

    Parameters
    ----------
    cluster_id : int
        Cluster ID.
    row : int
        Row.
    risk_value : int
        Risk value.

    Returns
    -------
    bool
        True if successful, False otherwise.
    """
    dao = DAO()
    df = dao.get_sequences_per_cluster(cluster_id)
    event_id = df.iloc[row].at["id_sequence"]
    try:
        dao.set_riskvalue(int(event_id), int(risk_value))
        return True
    except (ValueError, IndexError):
        return False


def set_cluster_name(cluster_id, cluster_name):
    """
    Set cluster name.

    Parameters
    ----------
    cluster_id : int
        Cluster ID.
    cluster_name : str
        Cluster name.

    Returns
    -------
    bool
        True if successful, False otherwise.
    """
    dao = DAO()
    try:
        dao.set_clustername(cluster_id=cluster_id, cluster_name=cluster_name)
        return True
    except (ValueError, IndexError):
        return False


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


def is_file_selected():
    """
    Check if a file is selected.

    Returns
    -------
    bool
        True if a file is selected, False otherwise.
    """
    dao = DAO()
    return 'emptyfile' != dao.display_selected_file()


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
    dataframe = formatSequenceCluster(cluster_id, "")
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
