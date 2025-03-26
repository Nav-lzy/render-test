import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from app.pages import home_page, genres_page, polarity_page, solo_collab_page, release_time_page, spotify_stats_page, shazam_page
from app.app import app

# Make sure the server instance is defined at the top
server = app.server  # Gunicorn will look for this

# Define the head
head = html.Div([

    # Title
    html.Div("Spotify Charts Analysis from 2017 to 2024",
             className="nav-title"),

    # Navbar
    html.Div([
        dcc.Link('Home', href='/', className="nav-link"),
        dcc.Link('Genres', href='/genres', className="nav-link"),
        dcc.Link('Polarity', href='/polarity', className="nav-link"),
        dcc.Link('Solo vs. Collaboration',
                 href='/solo_collab', className="nav-link"),
        dcc.Link('Release Time', href='/release_time', className="nav-link"),
        dcc.Link('Spotify Stats', href='/spotify_stats', className="nav-link"),
        dcc.Link('Shazam', href='/shazam', className="nav-link"),
    ], className="nav-links")
], className="navbar")

# Define the layout of the app
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    head,
    html.Div(id='page-content')
])

# Define the callback to display the correct page


@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def display_page(pathname):
    if pathname in ('', '/', 'home', ' '):
        return home_page.layout
    elif pathname == '/genres':
        return genres_page.layout
    elif pathname == '/polarity':
        return polarity_page.layout
    elif pathname == '/solo_collab':
        return solo_collab_page.layout
    elif pathname == '/release_time':
        return release_time_page.layout
    elif pathname == '/spotify_stats':
        return spotify_stats_page.layout
    elif pathname == '/shazam':
        return shazam_page.layout
    else:
        return html.H3("404 - Could not find page")


if __name__ == '__main__':
    app.run(debug=False)
