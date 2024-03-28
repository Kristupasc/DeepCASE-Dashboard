import dash
from dash import html, dash_table
import pandas as pd
import Dashboard.app.main.recources.loaddata as load
import Dashboard.app.main.recources.style as style

dash.register_page(__name__, path="/sequences", name="Sequences", title="Sequences", order=5)
df = load.formatSequence()

layout = html.Div([
    html.H1('Sequence')
    # ,
    # dash_table.DataTable(
    #     id='sequence',
    #     columns = [
    #         {'name': 'timestamp', 'id':'timestamp', 'type': 'any'},
    #         {'name': 'machine', 'id':'machine', 'type': 'any'},
    #         {'name': 'Event', 'id':'Event', 'type': 'numeric'},
    #         {'name': 'label', 'id':'label', 'type': 'numeric'},
    #         {'name': 'Context', 'id':'Context', 'type': 'any'}
    #         ],
    #     data=df.to_dict('records'),
    #     filter_action='native',
    #     style_data={
    #         'width': 'normal', 'minWidth': 'normal', 'maxWidth': 'normal',
    #         'overflow': 'hidden',
    #         'textOverflow': 'ellipsis',
    #     },
    #     page_size = 10)
    # https://dash.plotly.com/datatable/filtering


]#, style=style.content_style
)




