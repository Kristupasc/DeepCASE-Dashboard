from typing import Dict, Any
from Dashboard.data.dao.dao import *
import pandas as pd

format_time = "%H:%M:%S.%f, %d %b %Y" # For second %s %ssss
def get_cluster_id(cluster: str):
    dao = DAO()
    # df = dao.get_cluster_id(cluster)
    pass
def formatSequenceCluster(cluster: int, id_str: str)-> pd.DataFrame:
    dao = DAO()
    df = dao.get_sequences_per_cluster(cluster_id=cluster)
    df = df[df['id_cluster'] == cluster]
    df = df[['machine', 'timestamp',  'name','id_cluster', 'risk_label']]
    df['timestamp'] = pd.DatetimeIndex(pd.to_datetime(df['timestamp'], unit='s')).strftime(format_time)
    df['risk_label'] = pd.to_numeric(df['risk_label'])
    df['machine'] = pd.Series(df['machine'], dtype="string")
    df['name'] = pd.Series(df['name'], dtype="string")
    df['timestamp'] = pd.Series(df['timestamp'], dtype="string")
    df['id_cluster'] = pd.Series(df['id_cluster'], dtype="string")
    dict_id: dict[str, str] = dict()
    for i in df.columns:
        dict_id[i] = i + id_str
    df = df.rename(columns =dict_id)
    return df

def possible_clusters()-> [tuple]:
    dao = DAO()
    df = dao.get_clusters_result()
    df = df[['id_cluster', 'name_cluster']]
    df['id_cluster'] = pd.Series(df['id_cluster'], dtype="string")
    df['name_cluster'] = pd.Series(df['name_cluster'], dtype="string")
    df['name_cluster'].fillna(df['id_cluster'], inplace=True)
    df['id_cluster'] = pd.to_numeric(df['id_cluster'])
    df = list(df.itertuples(index=False, name=None))
    return df

def formatContext(cluster: int, index: int,id_str: str) -> pd.DataFrame:
    dao = DAO()
    df = dao.get_sequences_per_cluster(cluster).reindex()
    id_sequence = df.iloc[index].at["id_sequence"]
    df = dao.get_context_per_sequence(id_sequence)
    df["event"] = df["name"].apply(get_event_id)
    dict_id: dict[str, str] = dict()
    for i in df.columns:
        dict_id[i] = i + id_str
    df = df.rename(columns =dict_id)
    return df
def selectEventFormatted(cluster: int,index: int,id_str: str) -> pd.DataFrame:
    dao = DAO()
    df = dao.get_sequences_per_cluster(cluster).reindex()
    df = df.loc[[index]]
    df = df[['machine', 'timestamp',  'name','id_cluster', 'risk_label']]
    df['timestamp'] = pd.DatetimeIndex(pd.to_datetime(df['timestamp'], unit='s')).strftime(format_time)

    df['risk_label'] = pd.to_numeric(df['risk_label'])
    df['machine'] = pd.Series(df['machine'], dtype="string")
    df['name'] = pd.Series(df['name'], dtype="string")
    df['timestamp'] = pd.Series(df['timestamp'], dtype="string")
    df['id_cluster'] = pd.Series(df['id_cluster'], dtype="string")
    dict_id: dict[str, str] = dict()
    for i in df.columns:
        dict_id[i] = i + id_str
    df = df.rename(columns =dict_id)
    return df

def get_event_id(event_text):
    dao = DAO()
    df = dao.get_mapping()
    # look if it exists, it otherwise produces an error, catch it and return the same name.
    try:
        return df[df["name"] == event_text].iloc[0].at["id"]
    except:
        return event_text

def set_riskvalue(cluster_id, row,  risk_value):
    dao = DAO()
    df = dao.get_sequences_per_cluster(cluster_id)
    event_id =df.iloc[row].at["id_sequence"]
    return dao.set_riskvalue(event_id, risk_value)

