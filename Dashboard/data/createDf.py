import base64
import os

import dash
import pandas as pd
from dash import html
import io


# converts dataframe to csv and appends it to all_Sequences
def concat_csv(dataframe):
    dataframe.to_csv("new.csv", index=False)
    with open("new.csv", 'r') as f1:
        csv_to_add = f1.read()
    with open('sequence_data.csv', 'a') as f2:
        f2.write('\n')
        f2.write(csv_to_add)
    os.remove("new.csv")
    return

# Returns dash table with all stored data
def displayDataFile():
    if not os.path.isfile("sequence_data.csv"):
        # Return empty table if the data file is empty
        return dash.dash_table.DataTable()
    df = pd.read_csv("sequence_data.csv")
    return dash.dash_table.DataTable(
        # Return a table from data file
        df.to_dict('records'),
        [{'name': i, 'id': i} for i in df.columns]
    )


def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        # TODO add other possible inputs (e.g. xlsx)
        else:
            raise Exception('This file type is not supported')
        concat_csv(df)  # we have large csv
    except Exception as e:
        print(e)
        return html.Div([
            'An error occurred when processing this file. Check the required format of file: csv'
        ])

    return html.Div([
        html.H5(filename),
        displayDataFile()
    ])
