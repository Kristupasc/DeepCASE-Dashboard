import os
import dash
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import Dashboard.app.main.recources.style as style


from server import app, pao

from dash import Dash, html, dcc

GRAPH_INTERVAL = os.environ.get("GRAPH_INTERVAL", 5000)

#TODO: create and transfer to style file

#Define sidebar

def sidebar(active_index):
    active = [False] * 5
    # active[active_index] = True

    sidebar = html.Div( className = 'sidebar', children= [
            html.H1('DeepCASE', style={'textAlign': 'center', 'padding-bottom': 10}),
            html.Div([
                sidebar_button("database", "Database", active[3]),
                sidebar_button("dashboard", "Cluster view", active[0]),
                sidebar_button("manual-analysis", "Manual Analysis", active[1]),
                sidebar_button("semi-automatic", "Semi-auto Analysis", active[2]),
                sidebar_button("user-manual", "User Manual", active[4]),
            ])
        ]
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
            html.Div(className = 'sidebar-button', children=[
                html.Img(className = 'sidebar-button-img', src=img_path),
                html.Div([text], className = 'sidebar-button-text'),
                html.Img(className = 'sidebar-button-arrow', src=arrow),
            ],
                # style=style.sidebar_button_style_active if active else style.sidebar_button_style_inactive
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
    style=style.wrapper_style)

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





