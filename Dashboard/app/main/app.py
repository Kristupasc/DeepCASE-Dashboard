import os
import dash


from server import app

from dash import html, dcc

GRAPH_INTERVAL = os.environ.get("GRAPH_INTERVAL", 5000)


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
    ])


if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8050, debug=True)





