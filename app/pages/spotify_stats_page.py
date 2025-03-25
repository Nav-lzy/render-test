import dash
from dash import html, dcc

layout = html.Div([

        dcc.Location(id='url', refresh=False),

        html.H2("Spotify Stats"),

        html.Div([
            dcc.Link('Back', href='/', style={'marginRight': '20px'}),

        ], style={'marginTop': '20px'})
    ])
