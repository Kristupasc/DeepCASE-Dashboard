from dash import Dash
from Dashboard.processing.process_split import ProcessorAccessObject
from Dashboard.data.dao.database import Database

app = Dash(__name__, use_pages=True, suppress_callback_exceptions=True, meta_tags=[{'name': 'viewport',
                      'content': 'width=device-width, initial-scale=1.0'}])

pao = ProcessorAccessObject()
db = Database()
db.create_tables()

server = app.server