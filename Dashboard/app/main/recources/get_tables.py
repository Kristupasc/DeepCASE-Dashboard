import pandas as pd

from Dashboard.app.main.recources.setters_getters_cluster import get_event_id
from Dashboard.data.dao.dao import DAO

format_time = "%H:%M:%S.%f, %d %b %Y"  # For second %s %ssss
def get_initial_table():
    """
    Methode that returns the table that is uploaded

    Returns
    -------
    dataframe with file content
    """
    dao = DAO()
    return dao.get_initial_table()
def get_cluster_table(cluster: int, id_str: str) -> pd.DataFrame:
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
def get_context_table(cluster: int, index: int, id_str: str) -> pd.DataFrame:
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

def get_clusters_tuple() -> [tuple]:
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
