import base64
from datetime import datetime

import dash
import pandas as pd
from dash import html, dcc, callback
from Dashboard.data import createDf
import io
from dash.dependencies import Input, Output, State
import Dashboard.app.main.recources.style as style




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
    html.Div([
        dcc.Location(id='url', refresh=False),
        html.Div(id='output-data-upload')
    ]),
], style=style.content_style)


# Called when a user uploads a new file
@callback(Output('output-data-upload', 'children', allow_duplicate=True),
          Input('upload-data', 'contents'),
          State('upload-data', 'filename'),
          State('upload-data', 'last_modified'),
          prevent_initial_call=True
          )
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            createDf.parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children


# Called when at the start
@callback(Output('output-data-upload', 'children'),
          Input('url', 'pathname'))
def display_table(pathname):
    table = createDf.displayDataFile()
    return table
