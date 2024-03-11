import pandas as pd
def read_data(filepath):
    df = pd.read_csv(filepath)
    df.reindex
    return df
def concatTwoFiles(filepath1, filepath2):
    df1 = read_data(filepath1)
    df2 = read_data(filepath2)
    return pd.concat([df1, df2], axis=1, join='inner')
def formatSequence():
    df = concatTwoFiles('../../data/sequences.csv', '../../data/alerts.csv')
    df = df[['timestamp', 'machine', 'Event', 'label', 'Context']]
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
    df['label'] = pd.to_numeric(df['label'])
    df['Event'] = pd.to_numeric(df['Event'])
    return df