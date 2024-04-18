import random
import time
from threading import Thread

import pandas as pd

from Dashboard.app.main.recources.label_tools import choose_risk
from Dashboard.data.dao.dao import DAO
from Dashboard.processing.process_split import ProcessorAccessObject

format_time = "%H:%M:%S.%f, %d %b %Y"  # For second %s %ssss

process_going_on = False
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
    df = df[['machine', 'timestamp', 'name', 'risk_label', 'id_event']]
    df['timestamp'] = pd.DatetimeIndex(pd.to_datetime(df['timestamp'], unit='s')).strftime(format_time)
    df['risk_label'] = pd.to_numeric(df['risk_label'])
    df['machine'] = pd.Series(df['machine'], dtype="string")
    df['name'] = pd.Series(df['name'], dtype="string")
    df['timestamp'] = pd.Series(df['timestamp'], dtype="string")
    # df["id_event"] = df["name"].apply(get_event_id)
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
    df['name_cluster'] = df['name_cluster'].fillna(df['id_cluster'])
    df['id_cluster'] = pd.to_numeric(df['id_cluster'])
    df = list(df.itertuples(index=False, name=None))
    return df


def formatContext(cluster: int, index: int, id_str: str) -> pd.DataFrame:
    """
    Format the context DataFrame.

    :param cluster: the cluster ID
    :param index: index of the row
    :param id_str: ID string to uniquely identify the table
    :return: formatted DataFrame
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

    :param event_text: event text
    :return: event ID
    """
    dao = DAO()
    df = dao.get_mapping()
    # look if it exists, it otherwise produces an error, catch it and return the same name.
    try:
        return df[df["name"] == event_text].iloc[0].at["id"]
    except (ValueError, IndexError):
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
        dao.set_riskvalue(int(event_id), int(risk_value))
        return True
    except (ValueError, IndexError):
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
    except (ValueError, IndexError):
        return False


def start_automatic():
    """
    Runs automatic analysis.
    This use a thread in order to keep it running in background.
    Known bug in Dash.
    :return: object ProcessorAccessObject that runs automatic analysis
    """
    global process_going_on
    process_going_on = True
    pao = ProcessorAccessObject()
    thread = Thread(target=pao.run_automatic_mode())
    thread.start()
    thread2 = Thread(target=check_thread_alive(thread))
    thread2.start()
    return pao
def check_thread_alive(thread):
    global process_going_on
    while(thread.is_alive()):
        time.sleep(2)
    process_going_on = False


def get_risk_cluster(cluster_id):
    """
    Get the maximum risk label for a cluster.

    :param cluster_id: cluster ID
    :return: maximum risk label
    """
    dao = DAO()
    df = dao.get_sequences_per_cluster(cluster_id).reindex()
    df['risk_label'] = pd.to_numeric(df['risk_label'])
    return df['risk_label'].max()


def is_file_selected():
    """
    Check if a file is selected.

    :return: True if a file is selected, False otherwise
    """
    dao = DAO()
    return 'emptyfile' != dao.display_selected_file()


def get_algorithm_sequence(cluster_id):
    """
    Returns a list of row numbers where the value in column 'risk_label' is negative
    or where there is a unique combination['machine', 'risk_label', 'id_event'] of other specified columns.
    From the list a random element is selected.

    Parameters:
    :param: cluster_id to determine which cluster to be used.
    :return: number in the list of row numbers that meet the conditions.
    """
    dataframe = formatSequenceCluster(cluster_id, "")
    filtered_rows = []
    # Rows where value in column 'x' is negative
    negative_rows = dataframe.index[dataframe["risk_label"] < 0].tolist()
    filtered_rows.extend(negative_rows)
    # Rows with unique combinations of other specified columns
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
    Helper function, to get risk value
    :param cluster_id: the id of the cluster, where to get the risk value.

    :return: str representing the risk label.

    """
    return choose_risk(get_risk_cluster(cluster_id))


def get_algorithm_cluster():
    """
    Returns a random cluster_id that is selected as priority.

    Parameters:
    :param: cluster_id to determine which cluster to be used.
    :return: number in the list of row numbers that meet the conditions.
    """
    dao = DAO()
    df = dao.get_clusters_result()
    df["risk"] = df["id_cluster"].apply(function_risk)
    filter_name = ["Attack", "High", "Unlabeled"]
    # Filter rows based on 'risk' column
    filtered_rows = df[df['risk'].isin(filter_name)]
    # Extract 'id_cluster' values from filtered rows
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

    :return: random cluster ID
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

    :param cluster_id: cluster ID
    :return: random sequence index
    """
    dao = DAO()
    df = dao.get_sequences_per_cluster(cluster_id)
    rows = df.shape[0]
    rand = random.randrange(0, rows, 1)
    return rand


def get_row(cluster_id):
    """
    Get the max row number

    :param cluster_id: cluster ID
    :return: random sequence index
    """
    dao = DAO()
    df = dao.get_sequences_per_cluster(cluster_id)
    rows = df.shape[0]
    return rows
