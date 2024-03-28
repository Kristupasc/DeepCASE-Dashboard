from io import StringIO

import dash
from dash import html, dash_table, dcc, callback, Output, Input, ctx, State
import pandas as pd
from dash.exceptions import PreventUpdate
import plotly.graph_objs as go
import Dashboard.app.main.recources.loaddata as load
from Dashboard.app.main.recources.label_tools import choose_risk, get_colors
from Dashboard.data.dao.dao import DAO

########################################################################
#   Dashboard callback (All ids need to match 100%)               #
########################################################################
# suffix for all the ids that might be the same.
id_str = "_da"
cid_str = "_cida"
# Setting variables
cluster = 0
prev_row = -1
prev_graph = -1
prev_click = -1


@callback(
    Output('selected cluster' + id_str, "data"),
    Output('selected row' + id_str, "data"),
    Input("filter_dropdown" + id_str, "value")
)
def store_selected_cluster_and_row(state):
    """
    Store the selected cluster and row.

    :param state: the selected value from the filter dropdown
    :return: the selected cluster and row if they are integers
    """
    if isinstance(state, int):
        return state, None
    raise PreventUpdate


@callback(
    Output("dashboard", "data"),
    Input('selected cluster' + id_str, "data")
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


@callback(
    Output('Context information' + cid_str, "data"),
    Output('dashboard', 'page_current'),
    Output('dashboard', 'selected_rows'),
    Input('selected row' + id_str, "data"),
    Input('selected cluster' + id_str, "data"),
    Input('scatter-plot', 'clickData'),
    State('dashboard', 'page_current')
)
def display_context(row, cluster, click_data, current_page):
    """
    Display the context information based on the selected row and cluster.

    :param row: the selected row
    :param cluster: the selected cluster
    :param click_data: data from the click event on the scatter plot
    :return: the context frame as a dictionary of records
    """
    global prev_row
    global prev_graph
    # we check if the graph point was clicked or if the row was clicked in the table:
    is_graph_click = prev_graph != click_data and click_data is not None
    if not is_graph_click and row is not None and row != prev_row:
        # we load from what was clicked in the table
        df = load.formatContext(cluster, row, cid_str)
        prev_row = row
        return df.to_dict("records"), current_page, [row]  # Highlight the selected row in the dashboard table
    elif click_data is not None:
        # there was a graph click
        # we load from what was clicked in the graph
        point = int(click_data["points"][0]["pointIndex"])
        # now we need to find where the data is
        df = load.formatContext(cluster, point, cid_str)
        page_number = point // 10  # Assuming 10 entries per page
        # get the last number in the point
        prev_graph = click_data
        return df.to_dict("records"), page_number, [point]  # Highlight the clicked point in the dashboard table
    raise PreventUpdate


@callback(
    Output('scatter-plot', 'clickData'),
    Input('dashboard', 'selected_rows')
)
def highlight_selected_point(selected_rows):
    if selected_rows is not None and len(selected_rows) > 0:
        selected_point_index = selected_rows[0]  # Assuming only one row can be selected at a time
        return {"points": [{"pointIndex": selected_point_index}]}
    else:
        return None


def update_options_dropdown():
    """
    Update the options in the dropdown.

    :return: a list of options for the dropdown based on possible clusters with labels and values
    """
    return [{"label": i[1], "value": i[0]} for i in load.possible_clusters()]


def update_values_dropdown():
    """
    Update the values in the dropdown.
    :return: a list of values for the dropdown based on possible clusters
    """
    return list([i[0] for i in load.possible_clusters()])


@callback(
    Output('cluster name' + id_str, 'children'),
    Input('selected cluster' + id_str, "data")
)
def get_name_cluster(data):
    """
    Get the name of the selected cluster based on the cluster ID.

    :param data: the selected cluster ID
    :return: the name of the selected cluster or a default message if no cluster is selected
    """
    if isinstance(data, int):
        k = load.possible_clusters()
        for z in k:
            if z[0] == data:
                return z[1]
    return "Cluster not selected"


@callback(
    Output("scatter-plot", "figure"),
    Output("filter-buttons", "value"),
    [Input("filter_dropdown" + id_str, "value"),
     Input("scatter-plot", "clickData"),
     Input("filter-buttons", "value")]
)
def generate_scatter_plot(selected_cluster, click_data, filter_value):
    """
    Generate a scatter plot based on the selected cluster and highlight the clicked point.

    :param selected_cluster: the value selected in the filter dropdown
    :param click_data: data from the click event on the scatter plot
    :return: a dictionary containing the data and layout for the scatter plot
    """
    traces = []
    dao = DAO()
    x = []
    y = []
    colors_graph = []
    colors = get_colors()
    # check if selected_cluster is a list
    if not isinstance(selected_cluster, list):
        data = dao.get_sequences_per_cluster(selected_cluster)
        for sequence in data.to_dict('records'):
            timestamp = sequence["timestamp"]
            # convert the unix timestamp to date
            timestamp = pd.to_datetime(timestamp, unit='s')
            risk_label = sequence["risk_label"]
            x.append(timestamp)
            y.append(risk_label)
            colors_graph.append(colors["Risk Label"][choose_risk(int(risk_label))])
    else:
        filter_value = "All"

    global prev_click
    # Check if a point has been clicked
    if click_data and click_data != prev_click:
        prev_click = click_data
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
    }, filter_value
