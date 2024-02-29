import base64
from datetime import datetime

import dash
import pandas as pd
from dash import html, dcc, callback
from Dashboard.data import createDf
import io
from dash.dependencies import Input, Output, State

#TODO: create and transfer to style file

# Define the main content style
content_style = {
    'margin-left': '25%',
    'margin-right': '5%',
    'padding': '20px 10px'
}


dash.register_page(__name__, path="/database", name="Database", title="Database", order=3)

# layout = html.Div([
#     html.H1('Database'),
#     html.H2('All Sequences'),
#             html.Div(
#                 [
#                     dash.dash_table.DataTable(
#                         id='cluster-details',
#                         columns=[
#                             {"name": "Time", "id": "Time"},
#                             {"name": "Source", "id": "Source"},
#                             {"name": "Type", "id": "Type"},
#                             {"name": "Weight", "id": "Weight"},
#                             {"name": "Risk Label", "id": "Risk Label"}
#                         ],                        data=dummyData.df_clusters.to_dict('records'),
#                         style_table={'overflowY': 'auto'}
#                     )
#                 ],
#                 className="table",
#             )
#         ], style=content_style)

layout = html.Div([
    html.H1('Database'),
    html.H2('All Sequences'),
    dcc.Upload(
        id='upload-data',
        children=html.Button("Upload File"),
        # Allow multiple files to be uploaded
        multiple=True
    ),
    html.Div(id='output-data-upload'),
], style = content_style)

def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
    except Exception as e:
        print(e)
        return html.Div([
            'An error occurred when processing this file. Check the required format of file: csv'
        ])

    return html.Div([
        html.H5(filename),

        dash.dash_table.DataTable(
            df.to_dict('records'),
            [{'name': i, 'id': i} for i in df.columns]
        )
    ])

@callback(Output('output-data-upload', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              State('upload-data', 'last_modified'))
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children

