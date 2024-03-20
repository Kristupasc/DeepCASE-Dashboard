import base64
import os

import dash
import pandas as pd
from dash import html
import io
from Dashboard.data.dao.dao import DAO

global dao
dao = DAO()

#get csv file from dashboard
#fill in events table
#call DeepCASE to process file

#todo: concat files
def parse_contents(contents, filename, date):
    global dao
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
            df.to_csv('input_data.csv', mode='w')
        # TODO add other possible inputs (e.g. xlsx)
        else:
            raise Exception('This file type is not supported')
        dao.save_input(df)
    except Exception as e:
        print(e)
        return html.Div([
            'An error occurred when processing this file. Check the required format of file: csv'
        ])

    return html.Div([
        html.H5(filename),
        displayDataFile()
    ])

# Returns dash table with all stored data
def displayDataFile():
    global dao
    df = dao.get_initial_table()
    return dash.dash_table.DataTable(
        # Return a table from data file
        df.to_dict('records'),
        [{'name': i, 'id': i} for i in df.columns]
    )
