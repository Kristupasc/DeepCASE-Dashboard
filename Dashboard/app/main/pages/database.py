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



@callback(Output('output-data-upload', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              State('upload-data', 'last_modified'))
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            createDf.parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children

