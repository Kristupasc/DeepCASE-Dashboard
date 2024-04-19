import time

from dash import callback, no_update, ctx
from dash.dependencies import Input, Output, State

import Dashboard.app.main.recources.database_data as load
from Dashboard.data.upload import create_database

id_str = "_data"  # suffix for database IDs


@callback(
    Output("file-dropdown" + id_str, "options"),
    Input('url', 'pathname'),
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
    Output('file-dropdown' + id_str, 'value'),
    Output("feedback_switch" + id_str, 'opened'),
    Output("feedback_switch" + id_str, 'title'),
    Input('file-dropdown' + id_str, 'value'),
    State("feedback_switch" + id_str, 'opened'),
    prevent_initial_call=True)
def update_selected_file(value, opened):
    global progress_going_on
    if value is not None and not load.process_going_on:
        load.switch_file(value)
        return None, not opened, "File is changed"
    if load.process_going_on:
        return None, not opened, "Server is going on,\n\n please don't interrupted"
    return None, opened, "File unchanged"


@callback(Output("feedback_deepcase" + id_str, 'opened'),
          Output("feedback_deepcase" + id_str, 'title'),
          Output("loading output start deepcase", "children"),
          Input('start_deepcase_btn' + id_str, 'n_clicks'),
          State("feedback_deepcase" + id_str, 'opened'),
          prevent_initial_call=True)
def run_deepcase(n_clicks, opened):
    global process_going_on
    dao = time.sleep(0)
    if len((load.get_files()).values.flatten().tolist()) == 0 and 'start_deepcase_btn' + id_str == ctx.triggered_id:
        return not opened, "please upload a file", dao
    if 'start_deepcase_btn' + id_str == ctx.triggered_id and not load.is_file_selected():
        return not opened, "file is not selected", dao
    if 'start_deepcase_btn' + id_str == ctx.triggered_id and not load.process_going_on:
        load.process_going_on = True
        load.start_deepcase()
        return not opened, "DeepCASE process is finished. You can review results on Manual Analysis page.", dao
    elif 'start_deepcase_btn' + id_str == ctx.triggered_id:
        return not opened, "Server is busy", dao
    return opened, no_update, dao


@callback(Output("feedback_start_deepcase" + id_str, 'opened'),
          Input('start_deepcase_btn' + id_str, 'n_clicks'),
          State("feedback_start_deepcase" + id_str, 'opened'),
          prevent_initial_call=True
          )
def feedback_run_deepcase(n_clicks, opened):
    global progress_going_on
    if 'start_deepcase_btn' + id_str == ctx.triggered_id and not load.process_going_on and load.is_file_selected():
        return not opened
    return opened


@callback(
    Output("feedback_save_file" + id_str, 'opened'),
    Output("feedback_save_file" + id_str, 'title'),
    Input('upload-data' + id_str, 'contents'),
    State('upload-data' + id_str, 'filename'),
    State('upload-data' + id_str, 'last_modified'),
    State("feedback_save_file" + id_str, 'opened')
)
def store_file(list_of_contents, list_of_names, list_of_dates, opened):
    if list_of_contents is not None:
        text = [create_database.parse_contents(c, n, d) for c, n, d in
                zip(list_of_contents, list_of_names, list_of_dates)]
        return not opened, text
    return opened, "Nothing uploaded"


@callback(
    Output("uploaded data" + id_str, "data"),
    # Loading page
    Input('url', 'pathname'),
    # New file saved
    Input("feedback_save_file" + id_str, 'opened'),
    # New file selected
    Input("feedback_switch" + id_str, 'opened'),
prevent_initial_call=True
)
def update_table_input(url, input1, input2):
    return load.get_initial_table().to_dict('records')

@callback(
    Output('start_deepcase_btn' + id_str, 'disabled'),
    # Loading page
    Input('url', 'pathname'),
    # New file saved
    Input("feedback_save_file" + id_str, 'opened'),
    # New file selected
    Input("feedback_switch" + id_str, 'opened'),
)
def disable_button_security(in1, in2, in3):
    if load.is_file_selected():
        return bool(load.get_status_file())
    return True

