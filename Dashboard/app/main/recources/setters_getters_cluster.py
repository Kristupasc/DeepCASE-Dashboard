from Dashboard.data.dao.dao import DAO


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