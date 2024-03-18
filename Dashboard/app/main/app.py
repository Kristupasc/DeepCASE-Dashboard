import os
import dash
from dash.dependencies import Input, Output
import plotly.graph_objs as go

from Dashboard.data import dummyData
from server import app

from dash import Dash, html, dcc

GRAPH_INTERVAL = os.environ.get("GRAPH_INTERVAL", 5000)

#TODO: create and transfer to style file

#style
wrapper_style = {
    'font_family': 'Calibri'
}

# Define the sidebar style
sidebar_style = {
    'position': 'fixed',
    'top': 0,
    'left': 0,
    'bottom': 0,
    'width': '20%',
    'background-color': '#f8f9fa',
    'font-family': 'Calibri'
}

sidebar_button_style_active = {
    'width': '80%',
    'height': 50,
    'margin': 'auto',
    'border-radius': 8,
    'background-color': '#009999',
    'margin-bottom': 20,
    'color': '#FFFFFF',
}

sidebar_button_style_inactive = {
    'width': '80%',
    'height': 50,
    'margin': 'auto',
    'border-radius': 8,
    'background-color': '#FFFFFF',
    'margin-bottom': 20,
    'color': '#9197B3',
}

sidebar_button_img_style = {
    'height': 18,
    'float': 'left',
    'margin-left': 16,
    'margin-right': 20,
    'margin-top': 16,
}

sidebar_button_text_style = {
    'float': 'left',
    'font-size': 18,
    'padding-top': 14
}

sidebar_button_arrow_style = {
    'float': 'right',
    'height': 18,
    'margin-right': 10,
    'margin-top': 16,
}

#Define sidebar

def sidebar(active_index):
    active = [False, False, False, False]
    active[active_index] = True

    sidebar = html.Div(
        [
            html.H1('DeepCASE', style={'textAlign': 'center', 'padding-bottom': 10}),
            html.Div([
                sidebar_button("dashboard", "Dashboard", active[0]),
                sidebar_button("manual-analysis", "Manual Analysis", active[1]),
                sidebar_button("ai-analysis", "AI Analysis", active[2]),
                sidebar_button("database", "Database", active[3]),
            ])
        ],
        style=sidebar_style
    )

    return sidebar

def sidebar_button(link, text, active):
    if active:
        img_path = f"assets/{text.replace(' ','_').lower()}_active.svg"
        arrow = f"assets/arrow_active.svg"
    else:
        img_path = f"assets/{text.replace(' ', '_').lower()}_inactive.svg"
        arrow = f"assets/arrow_inactive.svg"

    return dcc.Link(
            html.Div([
                html.Img(src= img_path, style=sidebar_button_img_style),
                html.Div([text], style=sidebar_button_text_style),
                html.Img(src=arrow, style=sidebar_button_arrow_style),
            ],
                style=sidebar_button_style_active if active else sidebar_button_style_inactive
            ),
            href=link)


#Define space for the content of the pages
content = html.Div(dash.page_container, id='page-content')

#App layout
app.layout = html.Div([
    dcc.Location(id='url'),
    sidebar(1),
    content
    ],
    style=wrapper_style)

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





