import pandas as pd
def read_data(filepath):
    df = pd.read_csv(filepath)
    df.reindex
    return df
def concatTwoFiles(filepath1, filepath2):
    df1 = read_data(filepath1)
    df2 = read_data(filepath2)
    return pd.concat([df1, df2], axis=1, join='inner')