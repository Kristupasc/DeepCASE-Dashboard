import os
from dash import dcc, html, Dash, dash_table
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go

GRAPH_INTERVAL = os.environ.get("GRAPH_INTERVAL", 5000)

app = Dash(__name__)
app.title = "DeepCASE Dashboard"
app.config['suppress_callback_exceptions'] = True # This removes errors?? I don't get it but it works lol

server = app.server

# Define your color scheme
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

# Dummy data for clusters
clusters_data = [
    {"x": 1, "y": 10, "Risk Label": "Info"},
    {"x": 3.1, "y": 10.2, "Risk Label": "Info"},
    {"x": 3.9, "y": 10.5, "Risk Label": "Info"},
    {"x": 3, "y": 5, "Risk Label": "Medium"},
    {"x": 2, "y": 5, "Risk Label": "Low"},
    {"x": 9, "y": 3, "Risk Label": "Suspicious"},
    {"x": 10, "y": 6, "Risk Label": "Attack"},
    {"x": 4, "y": 1, "Risk Label": "High"},
    {"x": 1, "y": 1, "Risk Label": "Unlabeled"},
]

# Convert to DataFrame
df_clusters = pd.DataFrame(clusters_data)

# Define the main content style
content_style = {
    'margin-left': '25%',
    'margin-right': '5%',
    'padding': '20px 10px'
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

sidebar = html.Div(
    [
        html.H2('DeepCASE', className='display-4'),
        html.Hr(),
        html.Div([
            dcc.Link('Dashboard', href='/', className='btn btn-primary btn-lg btn-block'),
            html.Hr(),
            dcc.Link('Manual Analysis', href='/manual-analysis', className='btn btn-secondary btn-lg btn-block'),
            html.Hr(),
            dcc.Link('AI Analysis', href='/ai-analysis', className='btn btn-secondary btn-lg btn-block'),
            html.Hr(),
            dcc.Link('Database', href='/database', className='btn btn-secondary btn-lg btn-block'),
        ], className='nav flex-column')
    ],
    style=sidebar_style
)

#the main scatterplot for the clusters
plot = html.Div(
    [
        html.Div(
            [
                html.H6("DeepCASE Dashboard", className="graph__title"),
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
                dash_table.DataTable(
                    id='cluster-details',
                    columns=[{"name": i, "id": i} for i in df_clusters.columns],
                    data=df_clusters.to_dict('records'),
                    style_table={'height': '300px', 'overflowY': 'auto'}
                )
            ],
            className="table",
        ),
    ]
)

# Define the main content
content = html.Div(id='page-content', style=content_style)

# the layout consists of the sidebar and the content, which is bascially the graph and a table
app.layout = html.Div([dcc.Location(id='url'), sidebar, content])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def render_page_content(pathname):
    if pathname == '/':
        return plot
    elif pathname == '/manual-analysis':
        return html.Div([
            html.H6('Manual Analysis Page')
        ])
    elif pathname == '/ai-analysis':
        return html.Div([
            html.H6('AI Analysis Page')
        ])
    elif pathname == '/database':
        return html.Div([
            html.H6('Database Page')
        ])
    # If the user tries to reach a different page, return a 404 message
    return dcc.Jumbotron([
        html.H1('404: Not found', className='text-danger'),
        html.Hr(),
        html.P(f"The pathname {pathname} was not recognised...")
    ])

@app.callback(
    Output("scatter-plot", "figure"), [Input("scatter-update", "n_intervals")]
)
def generate_scatter_plot(interval):
    traces = []
    for cluster_name, cluster_group in df_clusters.groupby("Risk Label"):
        traces.append(
            go.Scatter(
                x=cluster_group["x"],
                y=cluster_group["y"],
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
            xaxis={"title": "X-axis"},
            yaxis={"title": "Y-axis"},
            margin={"l": 40, "b": 40, "t": 10, "r": 10},
            legend={"x": 0, "y": 1},
            hovermode="closest",
            transition={"duration": 500},
            plot_bgcolor=colors["background"],
            paper_bgcolor=colors["background"],
            font={"color": colors["text"]},
        ),
    }

if __name__ == "__main__":
    app.run_server(debug=True)