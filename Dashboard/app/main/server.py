from dash import Dash

app = Dash(__name__, use_pages=True, suppress_callback_exceptions=True, meta_tags=[{'name': 'viewport',
                      'content': 'width=device-width, initial-scale=1.0'}])
server = app.server
