import base64
import os

import dash
import pandas as pd
from dash import html
import io
from Dashboard.data.dao.dao import DAO
import Dashboard.app.main.recources.style as style


def parse_contents(contents: str, filename: str, date: float):
    """
    Parse the contents of the uploaded file.

    Parameters
    ----------
    contents : str
        The content of the uploaded file in base64.
    filename : str
        The name of the uploaded file.
    date : float
        The last modified date.

    Returns
    -------
    str
        A message indicating the success or failure of file processing.
    """
    dao = DAO()
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            input_df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
            input_df.to_csv('input_data.csv', mode='w')
        # TODO add other possible inputs (e.g. xlsx)
        else:
            return 'This file type is not supported'
        from_csv_df = pd.read_csv('input_data.csv')
        from_csv_df.drop(columns='Unnamed: 0', inplace=True)
        dao.save_input(from_csv_df, filename)  # fills events table

    except Exception as e:
        print(e)
        return 'An error occurred when processing this file.\n Check the required format of file: csv'
    return 'File Uploaded Successfully: ' + filename+'' \
                                                     '\n\n\nPress "Start Security Analysis" button to run DeepCASE.'



