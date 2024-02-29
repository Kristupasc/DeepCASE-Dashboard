import os
import dash
from dash.dependencies import Input, Output
import plotly.graph_objs as go

from Dashboard.data import dummyData
from server import app

from dash import Dash, html, dcc

GRAPH_INTERVAL = os.environ.get("GRAPH_INTERVAL", 5000)

#TODO: create and transfer to style file

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
#Define space for the content of the pages
content = html.Div(dash.page_container, id='page-content')

#App layout
app.layout = html.Div([
    dcc.Location(id='url'),
    sidebar,
    content
])

#TODO: rewrite 404 page s.t it is not shown on sidebar

#     # If the user tries to reach a different page, return a 404 message
#     return dcc.Jumbotron([
#         html.H1('404: Not found', className='text-danger'),
#         html.Hr(),
#         html.P(f"The pathname {pathname} was not recognised...")
#     ])
#



if __name__ == '__main__':
    app.run_server(debug=True)





