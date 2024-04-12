from io import StringIO
from math import floor
import dash
from dash import html, dash_table, dcc, callback, Output, Input, ctx, State, no_update
import pandas as pd
from dash.exceptions import PreventUpdate
import Dashboard.app.main.pagescallback.display_sequence as display_sequence
import Dashboard.app.main.recources.loaddata as load

########################################################################
#   Manual callback (All ids need to match 100%)               #
########################################################################
# suffix for all the ids that might be the same.
id_str = "_ma"
cid_str = "_cma"
qid_str = "-qma"
# Variables for all users
automatic_analysis = False
@callback(
    Output('selected cluster' + id_str, "data"),
    Input("filter_dropdown" + id_str, "value"),
    Input('random' + id_str, "n_clicks")
)
def store_selected_cluster(state, click):
    """
    Store the selected cluster based on dropdown value or random click.

    :param state: the value from the filter dropdown
    :param click: the number of clicks on the random button
    :return: the selected cluster or trigger a PreventUpdate exception
    """
    if 'random' + id_str == ctx.triggered_id:
        return load.get_random_cluster()
    if isinstance(state, int):
        return state
    raise PreventUpdate


@callback(
    Output("manual", "data"),
    Input('selected cluster' + id_str, "data")
)
def update_table_cluster(state):
    """
    Update the table in the manual component based on the selected cluster.

    :param state: the selected cluster ID
    :return: the formatted data for the table as a dictionary of records
    """
    if isinstance(state, int):
        dff = load.formatSequenceCluster(state, id_str)
        return dff.to_dict("records")
    raise PreventUpdate


@callback(
    Output('selected row' + id_str, "data"),
    Output('manual', 'selected_rows'),
    Output('manual', 'page_current'),  # this is for display the right page
    Input("manual", 'selected_rows'),
    Input('random' + qid_str, "n_clicks"),
    Input("selected cluster" + id_str, "data")
)
def store_context_row(state, click, cluster_id):
    """
    Store the context row based on user interactions and trigger events.

    :param state: the selected rows in the manual component
    :param click: the number of clicks on the random button
    :param cluster_id: the selected cluster ID
    :return: the stored context row or trigger a PreventUpdate exception,
    as well the updated row selected, page current.
    """
    if isinstance(cluster_id, int):
        if 'random' + qid_str == ctx.triggered_id and isinstance(cluster_id, int):
            state = load.get_random_sequence(cluster_id)
            return state, [state], floor(state / 10)
        if state is not None:
            if len(state) > 0:
                if isinstance(state[0], int):
                    rows = load.get_row(cluster_id)
                    state = [min(rows-1, state[0])]
                    return state[0], state, floor(state[0] / 10)
        raise PreventUpdate
    return None, [], None


@callback(
    Output('Context information' + cid_str, "data"),
    Input('selected row' + id_str, "data"),
    Input('selected cluster' + id_str, "data")
)
def display_context(row, cluster):
    """
    This function displays the context information based on the selected row and cluster.

    :param row: the selected row
    :param cluster: the selected cluster
    :return: the context frame as a dictionary of records
    """
    if isinstance(row, int) and isinstance(cluster, int) and row <= load.get_row(cluster):
        df = load.formatContext(cluster, row, cid_str)
        return df.to_dict("records")
    raise PreventUpdate


callback(
    Output("filter_dropdown" + id_str, 'options'),
    Input('change cluster name', 'n_clicks')
)(display_sequence.update_options_dropdown)
callback(
    Output("filter_dropdown" + id_str, 'value'),
    Input('change cluster name', 'n_clicks')
)(display_sequence.update_values_dropdown)


callback(
    Output('cluster name' + id_str, 'value'),
    Input('selected cluster' + id_str, "data")
)(display_sequence.get_name_cluster)

########################################################################################
# Editable callback extra functionality special for manual.
########################################################################################

@callback(
    Output("modal_set_cluster"+id_str, "opened"),
    Output("modal_set_cluster"+id_str, "title"),
    Input('selected cluster' + id_str, "data"),
    Input('change cluster name', 'n_clicks'),
    State('cluster name' + id_str, 'value'),
    State("modal_set_cluster"+ id_str, "opened"),
    prevent_initial_call = True,
)
def set_cluster_name(cluster_id, button, cluster_name, opened):
    """
    Set the label for the cluster based on user input and send an modal.

    :param cluster_id: the selected cluster ID
    :param n_clicks: the number of clicks on the change cluster name button
    :param value: the new value for the cluster name
    :param opened: send feedback if the pop up is opened
    :return: a message indicating the success of the operation or unchanged status, true if pop-up need to be shown.
    """
    if 'change cluster name' == ctx.triggered_id:
        if isinstance(cluster_id, int) and isinstance(cluster_name, str):
            if load.set_cluster_name(cluster_id, cluster_name):
                return not opened, "Succesfully changed to: "+cluster_name
        return not opened, "Nothing changed, please provide correct input"
    return opened, "nothing"



@callback(
    Output("modal_set_risk"+id_str, "opened"),
    Output("modal_set_risk"+id_str, "title"),
    Input('selected cluster' + id_str, "data"),
    Input('manual', "data"),
    Input('manual', "data_previous"),
    State('manual', 'active_cell'),
    State("modal_set_risk"+id_str, "opened"),
    prevent_initial_call=True
)
def set_risk_label(cluster, data, data_previous, active, opened):
    """
    Set the risk label based on user input.

    :param cluster: is the cluster selected.
    :param data: is all the data of the dash table, there don't exist a better parameter
    :param data_previous: is all the data of the dash table, before change.
    :param active: is the parameter that checks which cell is edited.
    (When you want to reconstruct to multiple cells to edit at the same time this should allow for a selection bigger.)
    This is an state because it needs a bit more dynamically.
    :param opened: provide feedback of the modal.
    :return: a message indicating the success of the operation
    """
    if data is not None and active is not None and cluster is not None:
        value = data[active['row']-1]['risk_label' + id_str]
        if verify_not_different_data(data, data_previous, active): # To prevent extra pop-up.
            if data_previous[active['row']-1]['risk_label' + id_str] != value:
                if isinstance(active['row'], int) and isinstance(cluster, int) and isinstance(value, int):
                    if load.set_riskvalue(cluster_id=cluster, row=active['row']-1, risk_value=value):
                        return not opened, "Successful, saved the row."
                return not opened, "Please provide correct values"
    return opened, "Nothing to be seen"

def verify_not_different_data(data, data_previous,active):
    """
    Verify if the cluster is changed, in a bit unconvined way.
    It is just to make sure that the user don't experience an anoying pop-up.
    It don't update unwanted values anyways.
    """
    check1 = data[active['row']-1]['timestamp' + id_str] ==  data_previous[active['row']-1]['timestamp' + id_str]
    check2 = data[active['row']-1]['machine' + id_str] ==  data_previous[active['row']-1]['machine' + id_str]
    return check2 and check1

########################################################################################
# Light up the selected row.
########################################################################################
callback(
    Output("manual", "style_data_conditional"),
    Input("selected row" + id_str, "data")
)(display_sequence.light_up_selected_row)

########################################################################################
# Start semi-automatic phase.
########################################################################################
@callback(Output("process of automatic"+id_str, 'data'),
          Output("feedback start automatic"+id_str, 'opened'),
          Output("feedback start automatic"+id_str, 'title'),
          Input('start automatic', 'n_clicks'),
          State("feedback start automatic"+id_str, 'opened'),
          prevent_initial_call=True,
          )
def start_run_automatic(n_clicks, opened):
    """

    This methode stores if the analysis need to start.
    :param n_clicks: is needed to verify a button press
    :param opened: Makes sure that the pop-up is not already displayed.

    :return:  Return pop-up with text.

    """
    if 'start automatic' == ctx.triggered_id:
        if load.is_file_selected():
            load.start_automatic()
            return True, not opened, "Automatic analysis is successful done."
        else:
            return False, not opened, "Please select a file"
    # No update otherwise it gets triggered again.
    return False, opened, "Not pressed button"
@callback( Output('start automatic', 'style'),
           Input('start automatic', 'n_clicks'),
        )
def hid_btn_run_automatic(n_clicks):
    if 'start automatic' == ctx.triggered_id:
        return {'display': 'none'}
    return {}
@callback(
    Output('feedback automatic', 'children'),
    Input('start automatic', 'n_clicks')
)
def feedBack_run_automatic(n_clicks):
    if 'start automatic' == ctx.triggered_id:
        return 'DeepCASE automatic phase is running.\n Please do not close this page until the process is finished. It may take several minutes.'
    return ''
########################################################################################
# Find the risk value of cluster and display
########################################################################################
callback(
    Output("display risk cluster"+id_str, "children"),
    Input('selected cluster' + id_str, "data")
)(display_sequence.display_risk_cluster)
