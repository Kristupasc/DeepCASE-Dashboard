import os
import dash
from dash import html, dcc

dash.register_page(__name__, path="/user-manual", name="User Manual", title="User Manual", order=0)
########################################################################
#                       User-manual page, from Markdown file.          #
########################################################################

# we need to get the location of the markdown file. We use absolute paths to make sure the file is found in docker.
# Get the directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the absolute path to the file using a raw string literal
file_path = os.path.join(current_dir, r'../../static/User_Manual_Interface_Usage_Guide.md')

with open(file_path, 'r') as instruction_file:
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
