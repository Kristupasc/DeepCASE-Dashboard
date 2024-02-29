import dash
from dash import html
from Dashboard.data import dummyData

#TODO: create and transfer to style file

# Define the main content style
content_style = {
    'margin-left': '25%',
    'margin-right': '5%',
    'padding': '20px 10px'
}



dash.register_page(__name__, path="/database", name="Database", title="Database", order=3)

layout = html.Div([
    html.H1('Database'),
    html.H6('All Sequences'),
            html.Div(
                [
                    dash.dash_table.DataTable(
                        id='cluster-details',
                        columns=[
                            {"name": "Date", "id": ""},
                            {"name": "Cluster", "id": "Cluster"},
                            {"name": "Type", "id": ""},
                            {"name": "Risk Label", "id": "Risk Label"}
                        ],                        data=dummyData.df_clusters.to_dict('records'),
                        style_table={'height': '300px', 'overflowY': 'auto'}
                    )
                ],
                className="table",
            )
        ])