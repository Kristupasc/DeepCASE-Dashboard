import base64
import os

import dash
import pandas as pd
from dash import html
import io
from Dashboard.data import dummyData
from datetime import datetime


# converts dataframe to csv and appends it to all_Sequences
def concat_csv(dataframe):
    csv_to_add = ""
    dataframe.to_csv("new.csv", index=False)
    # open the new.csv and iterate through each line and add a risk label to the line
    with open('new.csv', 'r') as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            if i == 0:
                continue
            # get the weight
            timestamp = datetime.utcfromtimestamp(float(line.split(',')[0]))
            weight = int(line.split(',')[3])
            csv_to_add += str(timestamp) + "," + line.split(',')[1] + "," + line.split(',')[2] + "," + str(weight) + "," + str(dummyData.choose_risk(weight * 10)) + "\n"
    # TODO Fix sequence_data path
    with open('sequence_data.csv', 'a') as f2:
        f2.write('\n')
        f2.write(csv_to_add)
    os.remove("new.csv")
    return


# Returns dash table with all stored data
def displayDataFile():
    # TODO Fix sequence_data path
    if not os.path.isfile("sequence_data.csv"):
        create_empty_data()
    df = pd.read_csv("sequence_data.csv")
    return dash.dash_table.DataTable(
        # Return a table from data file
        df.to_dict('records'),
        [{'name': i, 'id': i} for i in df.columns]
    )


def get_sequence_data_frame():
    # TODO Fix sequence_data path
    if not os.path.isfile("sequence_data.csv"):
        create_empty_data()
    return pd.read_csv("sequence_data.csv")


def create_empty_data():
    empty_data_frame = {
        'Time': [],
        'Type': [],
        'Source': [],
        'Weight': [],
        'Risk Label': []
    }
    df_clusters = pd.DataFrame(empty_data_frame)
    # TODO Fix sequence_data path
    df_clusters.to_csv("sequence_data.csv", index=False)
    return


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
