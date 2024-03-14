import pandas as pd
format_time = "%H:%M:%S.%f, %d %b %Y" # For second %s %ssss
def read_data(filepath):
    df = pd.read_csv(filepath)
    df.reindex
    return df
def concatTwoFiles(filepath1, filepath2):
    df1 = read_data(filepath1)
    df2 = read_data(filepath2)
    return pd.concat([df1, df2], axis=1, join='inner')
def concatMultipleFiles(filepaths: [str]):
    return pd.concat([read_data(filepath) for filepath in filepaths],axis=1, join='inner')
def formatSequence()-> pd.DataFrame:
    df = concatTwoFiles('../../data/sequences.csv', '../../data/alerts.csv')
    df = df[['timestamp', 'machine', 'Event','event', 'label', 'Context']]
    df['timestamp'] = pd.DatetimeIndex(pd.to_datetime(df['timestamp'], unit='s')).strftime(format_time)
    df['label'] = pd.to_numeric(df['label'])
    df['Event'] = pd.to_numeric(df['Event'])
    df['event'] = pd.Series(df['event'], dtype="string")
    df['Context'] = pd.Series(df['Context'], dtype="string")
    df['timestamp'] = pd.Series(df['timestamp'], dtype="string")
    return df
def formatSequenceCluster(cluster: str)-> pd.DataFrame:
    pass #TODO: some mapping
def formatSequenceCluster(cluster: int)-> pd.DataFrame:
    df = concatMultipleFiles(['../../data/sequences.csv', '../../data/alerts.csv', '../../data/clusters.csv'])

    df = df[df['clusters'] == 0]
    df = df[['timestamp', 'machine', 'Event','event', 'labels', 'Context']]
    df['timestamp'] = pd.DatetimeIndex(pd.to_datetime(df['timestamp'], unit='s')).strftime(format_time)
    df['labels'] = pd.to_numeric(df['labels'])
    # df['labels'] = pd.to_numeric(df['labels'])
    # df['clusters'] = pd.to_numeric(df['clusters'])
    df['Event'] = pd.to_numeric(df['Event'])
    df['event'] = pd.Series(df['event'], dtype="string")
    df['Context'] = pd.Series(df['Context'], dtype="string")
    df['timestamp'] = pd.Series(df['timestamp'], dtype="string")
    return df