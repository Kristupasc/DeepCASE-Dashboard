import dash
from dash import html, dcc
dash.register_page(__name__, path="/user-manual", name="User Manual", title="User Manual", order=0)
########################################################################
#                       User-manual page, from Markdown file.          #
########################################################################
with open('../static/User_Manual_Interface_Usage_Guide.md', 'r') as instruction_file:
    instructions = instruction_file.read()
    instruction_file.close()

layout = html.Div(className = 'content', children = [
    html.H1('User Manual: Interface Usage Guide'),
    html.Div(className = 'subcontent user_manual', children = [
        dcc.Markdown(
            instructions
        )
    ])
    ])