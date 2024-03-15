import os

import dash
import pandas as pd
from dash import html, dcc, callback, dash_table
from dash.dependencies import Input, Output, State
from Dashboard.data import dummyData, createDf
import plotly.graph_objs as go

# create csv x2
# upload through database
# make it cluster on dashboard

GRAPH_INTERVAL = os.environ.get("GRAPH_INTERVAL", 5000)

dash.register_page(__name__, path="/", name="Dashboard", title="Dashboard", order=0)

# Define the main content style
content_style = {
    'margin-left': '25%',
    'margin-right': '5%',
    'padding': '20px 10px'
}

# Define color scheme
colors = {
    "background": "#FFFFFF",  # white background
    "text": "#000000",  # black text for visibility
    "Risk Label": {
        "Info": "#45B6FE",  # blue
        "Low": "#FFD700",  # gold
        "Medium": "#FF8C00",  # darkorange
        "High": "#FF4500",  # orangered
        "Attack": "#DC143C",  # crimson
        "Suspicious": "#800080",  # purple
        "Unlabeled": "#808080"  # grey
    }
}

# the main scatterplot for the clusters
plot = html.Div(
    [
        html.Div(
            [
                html.H2("All Clusters", className="graph__title"),
                dcc.Graph(id="scatter-plot"),
                dcc.Interval(
                    id="scatter-update",
                    interval=int(GRAPH_INTERVAL),
                    n_intervals=0,
                ),
            ],
            className="graph",
        ),
        html.Div(
            [
                dash.dash_table.DataTable(
                    id='cluster-details',
                    columns=[
                        {"name": "Time", "id": "Time"},
                        {"name": "Source", "id": "Source"},
                        {"name": "Type", "id": "Type"},
                        {"name": "Weight", "id": "Weight"},
                        {"name": "Risk Label", "id": "Risk Label"}
                    ],
                    data=dummyData.df_clusters.to_dict('records'),
                    style_table={'height': '300px', 'overflowY': 'auto'}
                )
            ],
            className="table",
        ),
    ]
)

layout = html.Div([
    html.H1('Dashboard'),
], style=content_style)


# check if the datapoint in the scatterplot is clicked
@callback(
    Output('cluster-details', 'data'),
    [Input('scatter-plot', 'clickData')]
)
def display_click_data(clickData):
    if clickData is None:
        return
    # here we would get the data from the click and display it in the table
    # it looks something like this:
    # {'points': [{'curveNumber': 2, 'pointNumber': 26895, 'pointIndex': 26895, 'x': '2017-07-03 18:01:27.4085', 'y': 3, 'bbox': {'x0': 934.83, 'x1': 949.83, 'y0': 357.5, 'y1': 372.5}}]}


@callback(
    Output("scatter-plot", "figure"),
    [Input("scatter-update", "n_intervals")]
)
def generate_scatter_plot(interval):
    traces = []
    # data = dummyData.df_clusters

    data = createDf.get_sequence_data_frame()
    print(data)
    for cluster_name, cluster_group in data.groupby("Risk Label"):
        traces.append(
            go.Scatter(
                x=cluster_group["Time"],
                y=cluster_group["Weight"],
                mode='markers',
                opacity=0.7,
                marker={
                    'size': 15,
                    'line': {'width': 0.5, 'color': 'white'},
                    'color': colors["Risk Label"][cluster_name]
                },
                name=cluster_name
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
    }
