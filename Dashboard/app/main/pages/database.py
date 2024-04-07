import base64
from datetime import datetime
from threading import Thread

import dash
import pandas as pd
from dash import html, dcc, callback
from Dashboard.data.upload import create_database
import io
from dash.dependencies import Input, Output, State
import Dashboard.app.main.recources.style as style
from Dashboard.processing.process_split import ProcessorAccessObject
from Dashboard.data.dao.dao import DAO

dash.register_page(__name__, path="/database", name="Database", title="Database", order=3)
dao = DAO()

layout = html.Div(className = 'content', children=[
    html.H1('Database'),
    html.Div(className='subcontent', children=[
        html.H2('All Sequences'),
        html.Div(className='top-bar', children=[
        dcc.Upload(
            id='upload-data',
            children=html.Button("Upload File"),
            # Allow multiple files to be uploaded
            multiple=True
        ),
        dcc.Dropdown(
            id="file-dropdown",
            placeholder="-Select a file-",
            multi=False,
            clearable=False,
        ),
        ]),
    html.Div([
            dcc.Location(id='url', refresh=False),
            html.Div(id='output-data-upload')
        ])
    ])
])


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
            create_database.parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children


# Called when at the start => retrieves the events table
@callback(Output('output-data-upload', 'children'),
          Input('url', 'pathname'))
def display_table(pathname):
    table = create_database.displayDataFile()
    return table


@callback(
    Output('output-data-upload', 'children', allow_duplicate=True),
    Input('file-dropdown', 'value'),
    Input('url', 'pathname'),
    prevent_initial_call=True)
def update_selected_file(value, pathname):
    dao.switch_current_file(value)
    return display_table(pathname=pathname)


@callback(
    Output("file-dropdown", "options"),
    Input('output-data-upload', 'children'),
    Input('file-dropdown', 'value')
)
def update_options(children, value):
    return dao.get_filenames().values.flatten().tolist()


@callback(Output('deepcase-status-display', 'children', allow_duplicate=True),
          Input('start_deepcase_btn', 'n_clicks'),
          prevent_initial_call=True)
def run_deepcase(n_clicks):
    if n_clicks and n_clicks > 0:
        pao = ProcessorAccessObject()
        thread = Thread(target=pao.run_DeepCASE())
        thread.start()
        return "DeepCASE process is finished. You can review results on Manual Analysis page."
    return dash.no_update


@callback(
    Output('start_deepcase_btn', 'style'),
    Input('start_deepcase_btn', 'n_clicks'),
    prevent_initial_call=True

)
def hide_button(n_clicks):
    if n_clicks and n_clicks > 0:
        return {'display': 'none'}
    return {}


@callback(
    Output('deepcase-status-display', 'children'),
    Input('start_deepcase_btn', 'n_clicks')
)
def hide_button(n_clicks):
    if n_clicks and n_clicks > 0:
        return 'DeepCASE is running. Please do not close this page until the process is finished. It may take several minutes.'
    return dash.no_update

# @callback(
#     Output('deepcase-status-display', 'children'),
#     Input('status-interval', 'n_intervals')
# )
# def update_status(n_intervals):
#     pao = ProcessorAccessObject()
#     status = pao.status
#     print(pao.status)
#     return html.P(status.name)
