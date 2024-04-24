import time

from dash import callback, no_update, ctx
from dash.dependencies import Input, Output, State

import Dashboard.app.main.recources.database_data as load
from Dashboard.app.main.recources import create_database

id_str = "_data"  # suffix for database IDs


@callback(
    Output("file-dropdown" + id_str, "options"),
    Input('url', 'pathname'),
    Input("feedback_save_file" + id_str, 'opened'),
    Input("feedback_switch" + id_str, 'opened'),
)
def update_options_drop_files(in1: str, in2: int, in3: int)-> list:
    """
    Update the file dropdown options.

    Parameters are there for trigger.

    Returns
    -------
    list
        The file names as a list.
    """
    return (load.get_files()).values.flatten().tolist()


@callback(
    Output('file-dropdown' + id_str, 'value'),
    Output("feedback_switch" + id_str, 'opened'),
    Output("feedback_switch" + id_str, 'title'),
    Input('file-dropdown' + id_str, 'value'),
    State("feedback_switch" + id_str, 'opened'),
    prevent_initial_call=True)
def update_selected_file(value : int, opened: bool)->(int, bool, str):
    """
    Update the selected file.

    Parameters
    ----------
    value : str
        The selected file.
    opened : bool
        The state of the switch.

    Returns
    -------
    tuple
        The selected file value, the opposite state of the switch, and the switch title.
    """
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
def run_deepcase(n_clicks: int, opened: bool)-> (bool, str):
    """
    Run the DeepCASE process.

    Parameters
    ----------
    n_clicks : int
        The number of clicks.
    opened : bool
        The state of the switch.

    Returns
    -------
    tuple
        The opposite state of the switch, the switch title, and the loading output.
    """
    global process_going_on
    dao = time.sleep(0)
    if len((load.get_files()).values.flatten().tolist()) == 0 and 'start_deepcase_btn' + id_str == ctx.triggered_id:
        return not opened, "please upload a file", dao
    if 'start_deepcase_btn' + id_str == ctx.triggered_id and not load.is_file_selected():
        return not opened, "file is not selected", dao
    if 'start_deepcase_btn' + id_str == ctx.triggered_id and not load.process_going_on:
        load.process_going_on = True
        load.start_deepcase()
        load.process_going_on = False
        return not opened, "DeepCASE process is finished. You can review results on Manual Analysis page.", dao
    elif 'start_deepcase_btn' + id_str == ctx.triggered_id:
        return not opened, "Server is busy", dao
    return opened, no_update, dao


@callback(Output("feedback_start_deepcase" + id_str, 'opened'),
          Input('start_deepcase_btn' + id_str, 'n_clicks'),
          State("feedback_start_deepcase" + id_str, 'opened'),
          prevent_initial_call=True
          )
def feedback_run_deepcase(n_clicks: int, opened: bool) -> bool:
    """
    Provide feedback for DeepCASE process.

    Parameters
    ----------
    n_clicks : int
        The number of clicks.
    opened : bool
        The state of the switch.

    Returns
    -------
    bool
        The opposite state of the switch.
    """
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
def store_file(list_of_contents: [], list_of_names: [], list_of_dates: [], opened: bool) -> (bool, str):
    """
    Store the uploaded file.

    Parameters
    ----------
    list_of_contents : list
        The contents of the uploaded file.
    list_of_names : list
        The filenames.
    list_of_dates : list
        The last modified dates.
    opened : bool
        The state of the switch.

    Returns
    -------
    tuple
        The opposite state of the switch and the title.
    """
    global progress_going_on
    if list_of_contents is not None:
        if load.process_going_on:
            return not opened, "Please try again later, the server is busy."
        text = [create_database.parse_contents(c, n, d) for c, n, d in
                zip(list_of_contents, list_of_names, list_of_dates)]
        return not opened, text
    return opened, "Nothing uploaded"


@callback(
    Output("uploaded data" + id_str, "data"),
    Input('url', 'pathname'),
    Input("feedback_save_file" + id_str, 'opened'),
    Input("feedback_switch" + id_str, 'opened'),
    prevent_initial_call=True
)
def update_table_input(url: str, input1: bool, input2: bool) -> dict:
    """
    Update the table with uploaded data.

    Parameters
    ----------
    url : str
        The URL pathname.
    input1 : bool
        The state of the switch.
    input2 : bool
        The state of the switch.

    Returns
    -------
    dict
        The updated table data.
    """
    return load.get_initial_table().to_dict('records')


@callback(
    Output('start_deepcase_btn' + id_str, 'disabled'),
    Input('url', 'pathname'),
    Input("feedback_save_file" + id_str, 'opened'),
    Input("feedback_switch" + id_str, 'opened'),
    Input("feedback_deepcase" + id_str, 'opened'),
)
def disable_button_security(in1: str, in2: int, in3: int, in4: int)-> bool:
    """
    Disable the DeepCASE start button based on conditions.

    Parameters
    ----------
    in1 : str
        The URL pathname.
    in2 : bool
        The state of the switch.
    in3 : bool
        The state of the switch.
    in4 : bool
        The state of the switch.

    Returns
    -------
    bool
        The state of the button to be disabled.
    """
    if load.is_file_selected():
        return bool(load.get_status_file())
    return True
