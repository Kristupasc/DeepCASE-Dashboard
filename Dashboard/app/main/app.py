import os
import dash
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from Dashboard.data import dummyData
from server import app
from dash import Dash, html, dcc
import Dashboard.app.main.recources.style as style

GRAPH_INTERVAL = os.environ.get("GRAPH_INTERVAL", 5000)

#TODO: create and transfer to style file

#style
wrapper_style = {
    'font_family': 'Calibri'
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
                sidebar_button("semi-automatic", "AI Analysis", active[2]),
                sidebar_button("database", "Database", active[3]),
            ])
        ],
        style=style.sidebar_style
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
                html.Img(src= img_path, style=style.sidebar_button_img_style),
                html.Div([text], style=style.sidebar_button_text_style),
                html.Img(src=arrow, style=style.sidebar_button_arrow_style),
            ],
                style=style.sidebar_button_style_active if active else style.sidebar_button_style_inactive
            ),
            href=link)


#Define space for the content of the pages
content = html.Div(dash.page_container, id='page-content', style={"float": "left"})

#App layout
app.layout = html.Div([
    dcc.Location(id='url'),
    sidebar(0),
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





