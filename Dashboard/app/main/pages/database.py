import dash
from Dashboard.app.main.pagescallback.database import *
from dash import html, dcc, dash_table
import dash_mantine_components as dmc

dash.register_page(__name__, path="/database", name="Database", title="Database", order=3)

layout = html.Div(className='content', children=[
    html.H1('Database'),
    html.Div(className='subcontent', children=[
        html.Div(className='top-bar', children=[
            html.Div(id='parent-upload-data' + id_str,
                     children=[
                         dcc.Upload(
                             id='upload-data' + id_str,
                             children=html.Button("Upload File"),
                             # Allow multiple files to be uploaded
                             multiple=True
                         ), ]
                     ),

            dcc.Dropdown(
                id="file-dropdown" + id_str,
                placeholder="-Select a file-",
                multi=False,
                clearable=False,
            ),
        ]),
        html.Div([
            dcc.Location(id='url' + id_str, refresh=False),
            html.Button('Start Security Analysis', id='start_deepcase_btn' + id_str, disabled =True),
            dash_table.DataTable(
                id="uploaded data" + id_str,
                columns=[
                    {'name': 'id_event', 'id': 'id_event', 'type': 'text'},
                    {'name': 'filename', 'id': 'filename', 'type': 'text'},
                    {'name': 'timestamp', 'id': 'timestamp', 'type': 'text'},
                    {'name': 'machine', 'id': 'machine', 'type': 'text'},
                    {'name': 'event', 'id': 'event', 'type': 'text'},
                    {'name': 'label', 'id': 'label', 'type': 'text'}
                ],
                filter_action='native',
                style_data={
                    'width': 'normal', 'minWidth': 'normal', 'maxWidth': 'normal',
                    'overflow': 'hidden',
                    'textOverflow': 'ellipsis',
                    'table-layout': 'auto',
                    'font-size': '11px',
                },
                page_size=50
            ),
        ])
    ]),
    dmc.Modal(title="Yeeeeeeeeaaaaaaaa", id="feedback_deepcase" + id_str),
    dmc.Modal(title="DeepCASE is running.\n\n This might take 20 minutes.\n\n Enjoy a cup of tea in the meantime.", id="feedback_start_deepcase" + id_str,
              children=[dcc.Loading(
                      id="loading start deepcase",
                      children=[html.Div([html.Div(id="loading output start deepcase")])],
                      type="circle",
                      fullscreen=False
                  )]),
    dmc.Modal(title="Yeeeeeeeeaaaaaaaa", id="feedback_save_file" + id_str),
    dmc.Modal(title="noo", id="feedback_switch" + id_str),
])