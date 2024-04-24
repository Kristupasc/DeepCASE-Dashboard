from Dashboard.data.dao.dao import DAO


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
