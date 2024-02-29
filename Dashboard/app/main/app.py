import os
import dash
from dash import dcc, html, Dash, dash_table
from dash.dependencies import Input, Output
import plotly.graph_objs as go

from Dashboard.data import dummyData
from server import app
# from server import server

import dash
from dash import Dash, html, dcc

GRAPH_INTERVAL = os.environ.get("GRAPH_INTERVAL", 5000)

#TODO: create and transfer to style file

#Define color scheme
colors = {
    "background": "#FFFFFF",  # white background
    "text": "#000000",       # black text for visibility
    "Risk Label": {
        "Info": "#A9A9A9",   # grey
        "Low": "#FFD700",    # gold
        "Medium": "#FF8C00", # darkorange
        "High": "#FF4500",   # orangered
        "Attack": "#DC143C", # crimson
        "Suspicious": "#800080", # purple
        "Unlabeled": "#808080"  # grey
    }
}

# Define the sidebar style
sidebar_style = {
    'position': 'fixed',
    'top': 0,
    'left': 0,
    'bottom': 0,
    'width': '20%',
    'padding': '20px 10px',
    'background-color': '#f8f9fa'
}

#Define sidebar
sidebar = html.Div(
    [
        html.H2('DeepCASE', className='display-4'),
        html.Hr(),
        html.Div([
            html.Div([
                dcc.Link(f"{page['name']}", href=page["relative_path"], className='btn btn-primary btn-lg btn-block'),
                html.Hr()
            ]) for page in dash.page_registry.values()
        ], className='nav flex-column')
    ],
    style=sidebar_style
)

#App layout
app.layout = html.Div([
    sidebar,
    dash.page_container
])

if __name__ == '__main__':
    app.run(debug=True)

#





#the main scatterplot for the clusters
# plot = html.Div(
#     [
#         html.Div(
#             [
#                 html.H1("All Clusters", className="graph__title"),
#                 dcc.Graph(id="scatter-plot"),
#                 dcc.Interval(
#                     id="scatter-update",
#                     interval=int(GRAPH_INTERVAL),
#                     n_intervals=0,
#                 ),
#             ],
#             className="graph",
#         ),
#         html.Div(
#             [
#                 dash_table.DataTable(
#                     id='cluster-details',
#                     columns=[
#                         {"name": "Date", "id": ""},
#                         {"name": "Source", "id": "Cluster"},
#                         {"name": "Type", "id": ""},
#                         {"name": "Risk Label", "id": "Risk Label"}
#                     ],
#                     data=dummyData.df_clusters.to_dict('records'),
#                     style_table={'height': '300px', 'overflowY': 'auto'}
#                 )
#             ],
#             className="table",
#         ),
#     ]
# )
#
# # Define the main content
# content = html.Div(id='page-content', style=content_style)
#
# # the layout consists of the sidebar and the content, which is bascially the graph and a table
# # app.layout = html.Div([dcc.Location(id='url'), sidebar, content])
#
#
# # @app.callback(Output('page-content', 'children'),
# #               [Input('url', 'pathname')])
#
# #     # If the user tries to reach a different page, return a 404 message
# #     return dcc.Jumbotron([
# #         html.H1('404: Not found', className='text-danger'),
# #         html.Hr(),
# #         html.P(f"The pathname {pathname} was not recognised...")
# #     ])
#
# @app.callback(
#     Output("scatter-plot", "figure"), [Input("scatter-update", "n_intervals")]
# )
# def generate_scatter_plot(interval):
#     traces = []
#     for cluster_name, cluster_group in dummyData.df_clusters.groupby("Risk Label"):
#         traces.append(
#             go.Scatter(
#                 x=cluster_group["x"],
#                 y=cluster_group["y"],
#                 mode='markers',
#                 opacity=0.7,
#                 marker={
#                     'size': 15,
#                     'line': {'width': 0.5, 'color': 'white'},
#                     'color': colors["Risk Label"][cluster_name]
#                 },
#                 name=cluster_name
#             )
#         )
#
#     return {
#         "data": traces,
#         "layout": go.Layout(
#             xaxis={"title": "X-axis"},
#             yaxis={"title": "Y-axis"},
#             margin={"l": 40, "b": 40, "t": 10, "r": 10},
#             legend={"x": 0, "y": 1},
#             hovermode="closest",
#             transition={"duration": 500},
#             plot_bgcolor=colors["background"],
#             paper_bgcolor=colors["background"],
#             font={"color": colors["text"]},
#         ),
#     }
#
# if __name__ == "__main__":
#     app.run_server(debug=True)