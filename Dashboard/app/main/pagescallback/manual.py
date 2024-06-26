import time
from math import floor

import dash
from dash import callback, Output, Input, ctx, State
from dash.exceptions import PreventUpdate

import Dashboard.app.main.pagescallback.common as display_sequence
import Dashboard.app.main.recources.data_dao_combine as load

# Suffix for all the ids that might be the same
id_str = "_ma"
cid_str = "_cma"
qid_str = "_qma"

# Variables for all users
automatic_analysis = False


# Function to store the selected cluster based on dropdown value or random click
@callback(
    Output('selected cluster' + id_str, "data"),
    Input("filter_dropdown" + id_str, "value"),
    Input('random' + id_str, "n_clicks"),
    Input('next' + id_str, "n_clicks")
)
def store_selected_cluster(state: int, click: int, nbtn: int) -> int:
    """

    Parameters
    ----------
    state: int
      the value from the filter dropdown
    click: int
      the number of clicks on the random button
    nbtn: int
      for next cluster triggered.

    Returns
    -------
    the selected cluster or trigger a PreventUpdate exception

    """
    if 'random' + id_str == ctx.triggered_id:
        return load.get_random_cluster()
    if 'next' + id_str == ctx.triggered_id:
        return load.get_algorithm_cluster()
    if isinstance(state, int):
        return state
    raise PreventUpdate


# Function to update the table in the manual component based on the selected cluster
@callback(
    Output("manual", "data"),
    Input('selected cluster' + id_str, "data")
)
def update_table_cluster(state: int) -> dict:
    """
    Update the table in the manual component based on the selected cluster.
    Parameters
    ----------
    state: int
     the selected cluster ID

    Returns
    -------
    the formatted data for the table as a dictionary of records

    """
    if isinstance(state, int):
        dff = load.get_cluster_table(state, id_str)
        return dff.to_dict("records")
    raise PreventUpdate


# Function to store the context row based on user interactions and trigger events
@callback(
    Output('selected row' + id_str, "data"),
    Output('manual', 'selected_rows'),
    Output('manual', 'page_current'),
    Input("manual", 'selected_rows'),
    Input('random' + qid_str, "n_clicks"),
    Input('next' + qid_str, "n_clicks"),
    Input("selected cluster" + id_str, "data")
)
def store_context_row(state: int, click: int, nbtn: int, cluster_id: int) -> (int, [int], int):
    """
    Store the context row based on user interactions and trigger events.
    Parameters
    ----------
    state : int
     the selected rows in the manual component
    click: int
     the number of clicks on the random button for sequence
    nbtn : int
     the number of clicks on the next sequence button.
    cluster_id : int
     the number representing the cluster.

    Returns
    -------
    The row selected, the selected row in array, the page number belongs to the selected cluster.

    """
    if isinstance(cluster_id, int):
        if 'random' + qid_str == ctx.triggered_id and isinstance(cluster_id, int):
            state = load.get_random_sequence(cluster_id)
            return state, [state], floor(state / 10)
        if 'next' + qid_str == ctx.triggered_id and isinstance(cluster_id, int):
            state = load.get_algorithm_sequence(cluster_id)
            return state, [state], floor(state / 10)
        if state is not None:
            if len(state) > 0:
                if isinstance(state[0], int):
                    rows = load.get_row(cluster_id)
                    state = [min(rows - 1, state[0])]
                    return state[0], state, floor(state[0] / 10)
        raise PreventUpdate
    return None, [], None


# Function to display the context information based on the selected row and cluster
@callback(
    Output('Context information' + cid_str, "data"),
    Input('selected row' + id_str, "data"),
    Input('selected cluster' + id_str, "data")
)
def display_context(row: int, cluster: int) -> dict:
    """
     Display the context information based on the selected row and cluster.
    Parameters
    ----------
    row : int
    Represent the selected row in the tabel.
    cluster: int
    Represent the selected cluster

    Returns
    -------
    The context frame as a dictionary.
    """
    if isinstance(row, int) and isinstance(cluster, int) and row <= load.get_row(cluster):
        df = load.get_context_table(cluster, row, cid_str)
        return df.to_dict("records")
    raise PreventUpdate


# Function to update the options in the dropdown
callback(
    Output("filter_dropdown" + id_str, 'options'),
    Input('change cluster name', 'n_clicks')
)(display_sequence.update_options_dropdown)

# Function to update the values in the dropdown
callback(
    Output("filter_dropdown" + id_str, 'value'),
    Input('change cluster name', 'n_clicks')
)(display_sequence.update_values_dropdown)

# Function to get the cluster name
callback(
    Output('cluster name' + id_str, 'value'),
    Input('selected cluster' + id_str, "data"),
)(display_sequence.get_name_cluster)


# Function to set the label for the cluster based on user input and send a modal
@callback(
    Output("modal_set_cluster" + id_str, "opened"),
    Output("modal_set_cluster" + id_str, "title"),
    Input('selected cluster' + id_str, "data"),
    Input('change cluster name', 'n_clicks'),
    Input('cluster name' + id_str, 'value'),
    State("modal_set_cluster" + id_str, "opened"),
    prevent_initial_call=True,
)
def set_cluster_name(cluster_id: int, button: int, cluster_name: str, opened: bool) -> (bool, str):
    """
    Set the label for the cluster based on user input and send an modal.

    Parameters
    ----------
    cluster_id : int
    the selected cluster ID
    button : int
    the number of clicks on the change cluster name button
    cluster_name : str
    the new value for the cluster name
    opened : bool
    send feedback if the pop-up is opened

    Returns
    -------
    A message indicating the success of the operation or unchanged status, true if pop-up need to be shown.

    """
    if 'change cluster name' == ctx.triggered_id or "\n" in cluster_name:
        cluster_name = cluster_name.split("\n", 1)[0]
        if isinstance(cluster_id, int) and isinstance(cluster_name, str):
            if load.set_cluster_name(cluster_id, cluster_name):
                return not opened, "Successfully changed to: " + cluster_name
        return not opened, "Nothing changed, please provide correct input"
    return opened, "nothing"


# Function to set the risk label based on user input
@callback(
    Output("modal_set_risk" + id_str, "opened"),
    Output("modal_set_risk" + id_str, "title"),
    Input('selected cluster' + id_str, "data"),
    Input('manual', "data"),
    Input('manual', "data_previous"),
    State('manual', 'active_cell'),
    State("modal_set_risk" + id_str, "opened"),
    prevent_initial_call=True
)
def set_risk_label(cluster: int, data: [[]], data_previous: [[]], active: dict, opened: bool) -> (bool, str):
    """
    Set the risk label based on user input.

    Parameters
    ----------
    cluster : int
    data : [[]]
    A table with all information
    data_previous: [[]]
    The data of the previous time the function is called.
    active : dict
    A dict with the cells that are selected by the user.
    opened : bool
    If the modal(pop-up) is opened.
    Returns
    -------
    A message indicating the success of the operation
    """
    global process_going_on
    try:
        if data is not None and active is not None and cluster is not None and not load.process_going_on:
            value = data[active['row'] - 1]['risk_label' + id_str]
            if verify_not_different_data(data, data_previous, active):
                if data_previous[active['row'] - 1]['risk_label' + id_str] != value:
                    if isinstance(active['row'], int) and isinstance(cluster, int) and isinstance(value, int):
                        if load.set_riskvalue(cluster_id=cluster, row=active['row'] - 1, risk_value=value):
                            return not opened, "Successful, saved the row."
                    return not opened, "Please provide correct values"
    except IndexError:
        return opened, "It failed to update"
    return opened, "Nothing to be seen"


# Function to verify if the cluster is changed
def verify_not_different_data(data, data_previous, active):
    """
    This methode is there to reduce the previous methode length.
    Verify if the cluster is changed, in a bit unconvinced way.
    It is just to make sure that the user don't experience an annoying pop-up.
    It doesn't update unwanted values anyway.
    Parameters
    ----------
    data : [[]]
    table of data
    data_previous : [[]]
    table as it was previously
    active: dict
    the cell that was active

    Returns
    -------
    True if it looks different it might not.
    False if it is definitely different.

    """
    check1 = data[active['row'] - 1]['timestamp' + id_str] == data_previous[active['row'] - 1]['timestamp' + id_str]
    check2 = data[active['row'] - 1]['machine' + id_str] == data_previous[active['row'] - 1]['machine' + id_str]
    return check2 and check1


# Function to light up the selected row
callback(
    Output("manual", "style_data_conditional"),
    Input("selected row" + id_str, "data")
)(display_sequence.light_up_selected_row)


# Function to start semi-automatic phase
@callback(Output("process of automatic" + id_str, 'data'),
          Output("feedback finish automatic" + id_str, 'opened'),
          Output("feedback finish automatic" + id_str, 'title'),
          Output("loading output start automatic", "children"),
          Input('start automatic', 'n_clicks'),
          State("feedback finish automatic" + id_str, 'opened'),
          prevent_initial_call=True,
          )
def start_run_automatic(n_clicks: int, opened: bool) -> (bool, bool, str, object):
    """
    This method stores if the analysis need to start.
    Parameters
    ----------
    n_clicks : int
    is needed to verify a button press
    opened : bool
    Makes sure that the pop-up is not already displayed.
    Returns
    -------
    Return pop-up with text and  send signal id process going on as well signal to load.

    """
    global process_going_on
    dao = time.sleep(0)
    if 'start automatic' == ctx.triggered_id and not load.process_going_on:
        if load.is_file_selected():
            load.process_going_on = True
            load.start_automatic()
            load.process_going_on = False
            return True, not opened, "Automatic analysis is successful done.", dao
        else:
            return False, not opened, "Please select a file", dao
    elif 'start automatic' == ctx.triggered_id:
        return False, not opened, "Please wait the server is busy", dao
    # No update otherwise it gets triggered again.
    return False, opened, "Not pressed button", dao


@callback(
    Output("feedback start automatic" + id_str, 'opened'),
    Input('start automatic', 'n_clicks'),
    State("feedback start automatic" + id_str, "opened")
)
def feedBack_run_automatic(n_clicks: int, opened: bool) -> bool:
    """
    Runs the automatic analysis
    Parameters
    ----------
    n_clicks : int
    the amount of clicks
    opened : bool
    State if pop-up is opened

    Returns
    -------
    Signal to show pop-up

    """
    global progress_going_on
    if 'start automatic' == ctx.triggered_id:
        return not opened
    return opened


# Function to find the risk value of cluster and display
callback(
    Output("display risk cluster" + id_str, "children"),
    Input('selected cluster' + id_str, "data")
)(display_sequence.display_risk_cluster)
