from dash import Dash
from Dashboard.data.dao.database import Database

#initialize database when the program starts
db = Database()
db.create_tables()

app = Dash(__name__, use_pages=True, suppress_callback_exceptions=True, meta_tags=[{'name': 'viewport',
                      'content': 'width=device-width, initial-scale=1.0'}])
#start the server
server = app.server
