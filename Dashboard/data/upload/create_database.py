import base64
import os

import dash
import pandas as pd
from dash import html
import io
from Dashboard.data.dao.dao import DAO


def parse_contents(contents, filename, date):
    dao = DAO()
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            input_df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
            input_df.to_csv('input_data.csv', mode='w')
        # TODO add other possible inputs (e.g. xlsx)
        else:
            raise Exception('This file type is not supported')
        from_csv_df = pd.read_csv('input_data.csv')
        from_csv_df.drop(columns='Unnamed: 0', inplace=True)
        dao.save_input(from_csv_df, filename)  # fills events table

    except Exception as e:
        print(e)
        return html.Div([
            'An error occurred when processing this file. Check the required format of file: csv'
        ])

    return html.Div([
        html.H5('File Uploaded Successfully: ' + filename),
        html.Button('Start Security Analysis', id='start_deepcase_btn'),
        html.Hr(),
        displayDataFile()
    ])


# Returns dash table with all stored data
def displayDataFile():
    dao = DAO()
    df = dao.get_initial_table()
    return dash.dash_table.DataTable(
        # Return a table from data file
        df.to_dict('records'),
        [{'name': i, 'id': i} for i in df.columns]
    )
