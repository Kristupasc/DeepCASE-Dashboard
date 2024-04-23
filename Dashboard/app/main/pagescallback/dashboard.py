import pandas as pd
import plotly.graph_objs as go
from dash import callback, Output, Input, State, callback_context
from dash.exceptions import PreventUpdate

# Importing callback functions, data loading functions, and DAO
import Dashboard.app.main.pagescallback.common as display_sequence
import Dashboard.app.main.recources.loaddata as load
from Dashboard.app.main.recources.label_tools import choose_risk, get_colors
from Dashboard.data.dao.dao import DAO

# Setting suffixes for IDs
id_str = "_da"  # suffix for dashboard IDs
cid_str = "_cida"  # suffix for context information IDs

# Callback to store the selected cluster
callback(
    Output('selected cluster' + id_str, "data"),  # Output: selected cluster data
    Input("filter_dropdown" + id_str, "value")  # Input: value of filter dropdown
)(display_sequence.store_selected_cluster)


# Callback to update the table based on the selected cluster
@callback(
    Output("dashboard", "data"),  # Output: data for dashboard table
    Input('selected cluster' + id_str, "data")  # Input: selected cluster data
)
def update_table_cluster(state):
    """
    Update the dashboard table based on the selected cluster.

    :param state: the selected cluster
    :return: the updated table data if the cluster is an integer
    """
    if isinstance(state, int):
        dff = load.formatSequenceCluster(state, id_str)
        return dff.to_dict("records")
    raise PreventUpdate


# Callback to store the selected row
callback(
    Output('selected row' + id_str, "data"),  # Output: selected row data
    State("dashboard", 'selected_rows'),  # State: selected rows in dashboard table
    Input("selected cluster" + id_str, "data")  # Input: selected cluster data
)(display_sequence.store_context_row)


# Callback to handle scatter plot click data and update page and selected rows
@callback(
    Output('dashboard', 'page_current'),  # Output: current page of dashboard
    Output('dashboard', 'selected_rows'),  # Output: selected rows in dashboard
    Input('scatter-plot', 'clickData'),  # Input: click data from scatter plot
)
def display_context(click_data):
    """
    Display the context information based on the selected row and cluster.

    :param click_data: the data from the click event on the scatter plot
    """
    # check if the graph point was clicked
    if click_data is not None:
        # graph click detected, get the clicked point index
        point = int(click_data["points"][0]["pointIndex"])
        # calculate page number based on point index
        page_number = point // 10  # Assuming 10 entries per page
        # return the page number and the clicked point as selected row
        return page_number, [point]
    raise PreventUpdate


# Various callbacks for dropdown updates
@callback(
    Output("display risk cluster" + id_str, "children"),  # Output: Risk label of cluster
    Input('selected cluster' + id_str, "data")  # Inputs: selected cluster data
)(display_sequence.display_risk_cluster)
@callback(
    Output("filter_dropdown" + id_str, 'options'),  # Output: options for filter dropdown
    Input('refresh-data', 'n_intervals')  # Input: number of intervals for refresh
)(display_sequence.update_options_dropdown)
@callback(
    Output("filter_dropdown" + id_str, 'value'),  # Output: value for filter dropdown
    Input('url', 'pathname')  # Input: pathname from URL
)(display_sequence.update_values_dropdown)
# Callback to get the cluster name and display it in the dashboard
@callback(
    Output('cluster name' + id_str, 'children'),  # Output: children of cluster name component
    Input('selected cluster' + id_str, "data")  # Input: selected cluster data
)(display_sequence.get_name_cluster)
# Callback to interact with data and update scatter plot, filter buttons, and context information
@callback(
    Output("scatter-plot", "figure"),  # Output: figure for scatter plot
    Output("filter-buttons", "value"),  # Output: value for filter buttons
    Output('Context information' + cid_str, "data"),  # Output: context information data
    [Input('selected cluster' + id_str, "data"),  # Inputs: selected cluster data
     Input('dashboard', 'selected_rows'),  # Inputs: selected rows in dashboard table
     Input("filter-buttons", "value")]  # Inputs: value of filter buttons
)
def interact_with_data(selected_cluster, selected_row, filter_value):
    """
    Updates the scatter plot, the table, and the events table based on the user selection.
    The selection can happen either in the table or in the graph.
    Once a user selects something in the graph, the point is also automatically selected in the table and vice versa.

    :param selected_cluster: the selected cluster
    :param selected_row: the selected row in the table
    :param filter_value: the selected filter value
    """
    # get the trigger to determine the source of the callback
    triggered_input = callback_context.triggered[0]["prop_id"].split(".")[0]
    # if a row in a table is selected, then it's not a graph click
    if selected_row is None:
        click_data = None
        events = None
    else:
        # it's a graph click
        click_data = {"points": [{"pointIndex": selected_row[0]}]}
        df = load.formatContext(selected_cluster, selected_row[0], cid_str)
        events = df.to_dict("records")
    # start generating values for the scatter plot
    traces = []
    dao = DAO()
    x = []
    y = []
    colors_graph = []
    colors = get_colors()
    # check if a cluster is selected
    if selected_cluster is not None:
        data = dao.get_sequences_per_cluster(selected_cluster)
        for sequence in data.to_dict('records'):
            timestamp = sequence["timestamp"]
            # convert the unix timestamp to date
            timestamp = pd.to_datetime(timestamp, unit='s')
            risk_label = sequence["risk_label"]
            x.append(timestamp)
            y.append(risk_label)
            # chooses a color based on the label
            colors_graph.append(colors["Risk Label"][choose_risk(int(risk_label))])
    else:
        filter_value = "All"
    # if the trigger is the scatter plot (dashboard), set the filter value to custom and highlight the point
    if triggered_input == "dashboard":
        filter_value = "Custom"
        # Initialize color map to grey for all points
        colors_graph = [colors["Risk Label"]["Unlabeled"]] * len(x)
        # Highlight the clicked point
        point_index = click_data["points"][0]["pointIndex"]
        colors_graph[point_index] = colors["Risk Label"][choose_risk(int(y[point_index]))]
    # Filter points based on the selected category
    if filter_value != 'All' and filter_value != 'Custom':
        # set the color for the points that have the filter value
        colors_graph = [
            colors["Risk Label"][choose_risk(int(risk_label))] if choose_risk(int(risk_label)) == filter_value else
            colors["Risk Label"]["Unlabeled"] for risk_label in y]
    # append all the information to the graph
    traces.append(
        go.Scatter(
            x=x,
            y=y,
            mode='markers',
            opacity=0.7,
            marker={
                'size': 15,
                'line': {'width': 0.5, 'color': 'white'},
                'color': colors_graph,
            },
            name="Sda"
        )
    )
    return {
        "data": traces,
        "layout": go.Layout(
            xaxis={"title": "Timeline"},
            yaxis={"title": "Security score"},
            margin={"l": 40, "b": 40, "t": 10, "r": 10},
            legend={"x": 0, "y": 1},
            hovermode="closest",
            transition={"duration": 500},
            plot_bgcolor=colors["background"],
            paper_bgcolor=colors["background"],
            font={"color": colors["text"]},
        ),
    }, filter_value, events


# Callback to light up the selected row in the dashboard
callback(
    Output("dashboard", "style_data_conditional"),  # Output: style_data_conditional for dashboard table
    Input("selected row" + id_str, "data")  # Input: selected row data
)(display_sequence.light_up_selected_row)
