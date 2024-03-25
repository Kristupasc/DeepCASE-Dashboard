import random
from typing import Dict, Any
from Dashboard.data.dao.dao import *
import pandas as pd

format_time = "%H:%M:%S.%f, %d %b %Y"  # For second %s %ssss


def formatSequenceCluster(cluster: int, id_str: str) -> pd.DataFrame:
    """
    Format the sequence cluster DataFrame.

    :param cluster: the cluster ID
    :param id_str: ID string to unique identify the table
    :return: formatted DataFrame
    """
    dao = DAO()
    df = dao.get_sequences_per_cluster(cluster_id=cluster)
    df = df[df['id_cluster'] == cluster]
    df = df[['machine', 'timestamp', 'name', 'risk_label']]
    df['timestamp'] = pd.DatetimeIndex(pd.to_datetime(df['timestamp'], unit='s')).strftime(format_time)
    df['risk_label'] = pd.to_numeric(df['risk_label'])
    df['machine'] = pd.Series(df['machine'], dtype="string")
    df['name'] = pd.Series(df['name'], dtype="string")
    df['timestamp'] = pd.Series(df['timestamp'], dtype="string")
    df["id_event"] = df["name"].apply(get_event_id)
    df['id_event'] = pd.Series(df['id_event'], dtype="string")
    dict_id: dict[str, str] = dict()
    for i in df.columns:
        dict_id[i] = i + id_str
    df = df.rename(columns=dict_id)
    return df


def possible_clusters() -> [tuple]:
    """
    Get possible clusters.

    :return: list of cluster tuples
    """
    dao = DAO()
    df = dao.get_clusters_result()
    df = df[['id_cluster', 'name_cluster']]
    df['id_cluster'] = pd.Series(df['id_cluster'], dtype="string")
    df['name_cluster'] = pd.Series(df['name_cluster'], dtype="string")
    df['name_cluster'].fillna(df['id_cluster'], inplace=True)
    df['id_cluster'] = pd.to_numeric(df['id_cluster'])
    df = list(df.itertuples(index=False, name=None))
    return df


def formatContext(cluster: int, index: int, id_str: str) -> pd.DataFrame:
    """
    Format the context DataFrame.

    :param cluster: the cluster ID
    :param index: index
    :param id_str: ID string to uniquely identify the table
    :return: formatted DataFrame
    """
    dao = DAO()
    df = dao.get_sequences_per_cluster(cluster).reindex()
    id_sequence = df.iloc[index].at["id_sequence"]
    df = dao.get_context_per_sequence(id_sequence)
    df["event"] = df["name"].apply(get_event_id)
    dict_id: dict[str, str] = dict()
    for i in df.columns:
        dict_id[i] = i + id_str
    df = df.rename(columns=dict_id)
    return df


def selectEventFormatted(cluster: int, index: int, id_str: str) -> pd.DataFrame:
    """
    Select and format an event DataFrame.

    :param cluster: the cluster ID
    :param index: index
    :param id_str: ID string to uniquely identify the table.
    :return: formatted DataFrame
    """
    dao = DAO()
    df = dao.get_sequences_per_cluster(cluster).reindex()
    df = df.loc[[index]]
    df = df[['machine', 'timestamp', 'name', 'id_cluster', 'risk_label']]
    df['timestamp'] = pd.DatetimeIndex(pd.to_datetime(df['timestamp'], unit='s')).strftime(format_time)
    df['risk_label'] = pd.to_numeric(df['risk_label'])
    df['machine'] = pd.Series(df['machine'], dtype="string")
    df['name'] = pd.Series(df['name'], dtype="string")
    df['timestamp'] = pd.Series(df['timestamp'], dtype="string")
    df["id_event"] = df["name"].apply(get_event_id)
    df['id_event'] = pd.Series(df['id_event'], dtype="string")
    dict_id: dict[str, str] = dict()
    for i in df.columns:
        dict_id[i] = i + id_str
    df = df.rename(columns=dict_id)
    return df


def get_event_id(event_text):
    """
    Get event ID.

    :param event_text: event text
    :return: event ID
    """
    dao = DAO()
    df = dao.get_mapping()
    # look if it exists, it otherwise produces an error, catch it and return the same name.
    try:
        return df[df["name"] == event_text].iloc[0].at["id"]
    except:
        return event_text


def set_riskvalue(cluster_id, row, risk_value):
    """
    Set risk value.

    :param cluster_id: cluster ID
    :param row: row
    :param risk_value: risk value
    :return: True if successful, False otherwise
    """
    dao = DAO()
    df = dao.get_sequences_per_cluster(cluster_id)
    event_id = df.iloc[row].at["id_sequence"]
    try:
        dao.set_riskvalue(event_id, risk_value)
        return True
    except:
        return False


def set_cluster_name(cluster_id, cluster_name):
    """
    Set cluster name.

    :param cluster_id: cluster ID
    :param cluster_name: cluster name
    :return: True if successful, False otherwise
    """
    dao = DAO()
    try:
        dao.set_clustername(cluster_id=cluster_id, cluster_name=cluster_name)
        return True
    except:
        return False


def get_random_cluster():
    """
    Get a random cluster.

    :return: random cluster ID
    """
    dao = DAO()
    df = dao.get_clusters_result()
    rows = df.shape[0]
    rand = random.randrange(0, rows, 1)
    return df.iloc[rand].at["id_cluster"]


def get_random_sequence(cluster_id):
    """
    Get a random sequence.

    :param cluster_id: cluster ID
    :return: random sequence index
    """
    dao = DAO()
    df = dao.get_sequences_per_cluster(cluster_id)
    rows = df.shape[0]
    rand = random.randrange(0, rows, 1)
    return rand
