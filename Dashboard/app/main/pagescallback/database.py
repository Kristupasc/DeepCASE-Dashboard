from dash import callback, no_update, ctx
from Dashboard.data.upload import create_database
import io
from dash.dependencies import Input, Output, State
import Dashboard.app.main.recources.style as style
from Dashboard.processing.process_split import ProcessorAccessObject
import base64
from datetime import datetime
from threading import Thread
import pandas as pd
import Dashboard.app.main.recources.database_data as load
id_str = "_data"  # suffix for database IDs

@callback(
    Output("file-dropdown"+id_str, "options"),
    Input('url' + id_str, 'pathname'),
    # New file saved
    Input("feedback_save_file" + id_str, 'opened'),
    # New file selected
    Input("feedback_switch" + id_str, 'opened'),
)
def update_options_drop_files(in1, in2, in3):
    """

    Parameters are there for trigger.
    :param children:
    :param value: value dropdown.

    :return: the file names as a list.

    """
    return (load.get_files()).values.flatten().tolist()

@callback(
    Output("feedback_switch" + id_str, 'opened'),
    Output("feedback_switch" + id_str, 'title'),
    Input('parent-upload-data' + id_str, "n_click"),
    State('file-dropdown'+id_str, 'value'),
    State("feedback_switch" + id_str, 'opened'),

    prevent_initial_call=True)
def update_selected_file(n_click,value, opened):
    if value is not None and n_click is not None:
        load.switch_file(value)
        return not opened, "File is changed"
    return opened, "File unchanged"

@callback(Output("feedback_deepcase" + id_str, 'opened'),
          Output("feedback_deepcase" + id_str, 'title'),
          Input('start_deepcase_btn'+id_str, 'n_clicks'),
          State("feedback_deepcase" + id_str, 'opened'),
          prevent_initial_call=True)
def run_deepcase(n_clicks, opened):
    if len((load.get_files()).values.flatten().tolist()) == 0 and 'start_deepcase_btn'+id_str == ctx.triggered_id:
        return not opened, "please upload a file"
    if 'start_deepcase_btn'+id_str == ctx.triggered_id and not load.is_file_selected():
        return not opened, "file is not selected"
    if 'start_deepcase_btn'+id_str == ctx.triggered_id and not load.process_going_on:
        load.start_deepcase()
        return not opened, "DeepCASE process is finished. You can review results on Manual Analysis page."
    elif 'start_deepcase_btn'+id_str == ctx.triggered_id:
        return not opened, "Server is busy"
    return opened, no_update
@callback(
    Output("feedback_save_file" + id_str, 'opened'),
    Output("feedback_save_file" + id_str, 'title'),
    Input('upload-data' + id_str, 'contents'),
    State('upload-data' + id_str, 'filename'),
    State('upload-data' + id_str, 'last_modified'),
    State("feedback_save_file" + id_str, 'opened')
)
def store_file( list_of_contents, list_of_names, list_of_dates, opened):
    if list_of_contents is not None:
        text = [create_database.parse_contents(c, n, d) for c, n, d in
                    zip(list_of_contents, list_of_names, list_of_dates)]
        return not opened, text
    return opened, "Nothing uploaded"

@callback(
    Output("uploaded data"+id_str, "data"),
    #Loading page
    Input('url' + id_str, 'pathname'),
    # New file saved
    Input("feedback_save_file" + id_str, 'opened'),
    # New file selected
    Input("feedback_switch" + id_str, 'opened'),
    prevent_initial_call=True
)
def update_table_input(url, input1, input2):
    return load.get_initial_table().to_dict('records')