import pandas as pd
from dash import dcc, html, Input, Output
import plotly.express as px
from collections import Counter
from app import app
from io import BytesIO
from wordcloud import WordCloud
import base64
from pathlib import Path


csv_path = Path(__file__).resolve(
).parents[2] / 'data' / 'global_17-24_final.csv'
df = pd.read_csv(csv_path)


# Extract all years
all_years = sorted(df['year'].unique())

# Extract all artists and get the top 15 based on appearing
artists_list = [artist.strip() for artists in df['artist_names']
                for artist in artists.split(',')]
artist_counts = Counter(artists_list)
top_15_artists = [artist for artist, _ in artist_counts.most_common(15)]

# Create the wordcloud


def generate_wordcloud_from_lyrics(text):
    wordcloud = WordCloud(width=800, height=400,
                          background_color='black').generate(text)

    # Save to a BytesIO buffer
    img = BytesIO()
    wordcloud.to_image().save(img, format='PNG')
    img.seek(0)

    # Encode image to base64
    img_base64 = base64.b64encode(img.read()).decode('utf-8')
    return f"data:image/png;base64,{img_base64}"


# Layout
layout = html.Div([
    # Wrapper Div für whole content
    html.Div([
        # First row
        html.Div([
            # Wordcloud
            html.Div([
                html.H3("Most used words in lyrics per year",
                        style={'color': 'white'}),
                dcc.Dropdown(
                    id='year-dropdown-wordcloud',
                    options=[{'label': str(year), 'value': str(year)}
                             for year in all_years],
                    value='2020',
                    style={
                        'width': '100%',
                        'backgroundColor': 'white',
                        'color': 'black',
                        'border': '1.5px solid #444',
                        'font-size': '14px',
                        'padding': '3px'
                    }
                ),
                html.Div(id='wordcloud-container',
                         style={'width': '100%', 'height': '400px'}),
            ], style={'flex': '1 1 48%', 'marginBottom': '30px', 'padding': '10px'}),

            # Top 5 highest and lowest polarity Songs
            html.Div([
                html.H3("Top 5 songs with highest and lowest polarity per year", style={
                        'color': 'white'}),
                dcc.Dropdown(
                    id='year-dropdown-top5',
                    options=[{'label': str(year), 'value': str(year)}
                             for year in all_years],
                    value='2020',
                    style={
                        'width': '100%',
                        'backgroundColor': 'white',
                        'color': 'black',
                        'border': '1.5px solid #444',
                        'font-size': '14px',
                        'padding': '3px'
                    }
                ),
                dcc.Graph(id='polarity-graph-top-bottom',
                          style={'height': '400px'}),
            ], style={'flex': '1 1 48%', 'marginBottom': '30px', 'padding': '10px'}),

        ], style={
            'display': 'flex',
            'flexWrap': 'wrap',
            'justifyContent': 'space-between',
            'padding': '20px',
            'gap': '20px'
        }),

        # Second row
        html.Div([
            # Polarity of songs per month
            html.Div([
                html.H3("Polarity of songs per month",
                        style={'color': 'white'}),
                dcc.Dropdown(
                    id='year-dropdown',
                    options=[{'label': str(year), 'value': str(year)}
                             for year in all_years],
                    value='2020',
                    style={
                        'width': '100%',
                        'backgroundColor': 'white',
                        'color': 'black',
                        'border': '1.5px solid #444',
                        'font-size': '14px',
                        'padding': '3px'
                    }
                ),
                dcc.Graph(id='polarity-graph', style={'height': '400px'}),
            ], style={'flex': '1 1 48%', 'marginBottom': '30px', 'padding': '10px'}),

            # Polarity and duration of top 50 artists
            html.Div([
                html.H3("Polarity and duration of top 50 artists",
                        style={'color': 'white'}),
                dcc.Dropdown(
                    id='year-dropdown-top50',
                    options=[{'label': str(year), 'value': str(year)}
                             for year in all_years],
                    value='2020',
                    style={
                        'width': '100%',
                        'backgroundColor': 'white',
                        'color': 'black',
                        'border': '1.5px solid #444',
                        'font-size': '14px',
                        'padding': '3px'
                    }
                ),
                dcc.Graph(id='polarity-graph-top-50',
                          style={'height': '400px'}),
            ], style={'flex': '1 1 48%', 'marginBottom': '30px', 'padding': '10px'}),

        ], style={
            'display': 'flex',
            'flexWrap': 'wrap',
            'justifyContent': 'space-between',
            'padding': '20px',
            'gap': '20px'
        }),

        # Third row
        html.Div([
            # Polarity of songs from top 15 artists over all years
            html.H3("Polarity of songs from top 15 artists over all years", style={
                    'color': 'white'}),
            dcc.Dropdown(
                id='artist-dropdown',
                options=[{'label': artist, 'value': artist}
                         for artist in top_15_artists],
                multi=True,
                value=[top_15_artists[0], top_15_artists[1]],
                style={
                    'width': '100%',
                    'backgroundColor': 'white',
                    'color': 'black',
                    'border': '1.5px solid #444',
                    'font-size': '14px',
                    'padding': '5px'
                }
            ),
            dcc.Graph(id='polarity-graph-artist', style={'height': '400px'}),
        ], style={'marginBottom': '30px', 'padding': '10px'}),

    ])
])

# Callbacks to update diagrams


@app.callback(
    Output('wordcloud-container', 'children'),
    Input('year-dropdown-wordcloud', 'value')
)
def update_wordcloud(selected_year):
    # Filter the selected year
    df_year = df[df['year'].astype(str) == selected_year]

    # Combine all lyrics to a text
    lyrics_text = ' '.join(df_year['lyrics'].dropna())

    # Generate the word cloud
    img_src = generate_wordcloud_from_lyrics(lyrics_text)

    # Return word cloud as a picture
    return html.Img(src=img_src, style={'width': '100%', 'height': '100%'})


@app.callback(
    Output('polarity-graph-top-bottom', 'figure'),
    Input('year-dropdown-top5', 'value')
)
def update_top5_songs(selected_year):
    # Filter the selcted year
    df_year = df[df['year'].astype(str) == selected_year]

    # Only show the first artist for reaons of space
    def get_main_artist(artist_names):
        artist_list = [artist.strip() for artist in artist_names.split(',')]
        return artist_list[0] + ", ..." if len(artist_list) > 1 else artist_list[0]

    # Apply the function on artist column
    df_year['main_artist'] = df_year['artist_names'].apply(get_main_artist)

    # Shorten the track names
    def shorten_track_name(track_name):
        if "(" in track_name:
            return track_name.split("(")[0].strip()
        return track_name

    # Apple the function on track column
    df_year['shortened_track_name'] = df_year['track_name'].apply(
        shorten_track_name)

    # Get the 5 highest and lowest polarity songs
    top_polarity = df_year.loc[df_year.groupby('main_artist')['polarity'].idxmax()][[
        'main_artist', 'shortened_track_name', 'polarity']]
    bottom_polarity = df_year.loc[df_year.groupby('main_artist')['polarity'].idxmin()][[
        'main_artist', 'shortened_track_name', 'polarity']]

    # Select the 5 highest and lowest polarity songs
    top_polarity = top_polarity.nlargest(5, 'polarity')
    bottom_polarity = bottom_polarity.nsmallest(5, 'polarity')

    # Mark the polarity types with positive and negative
    top_polarity["Polarity Type"] = "Positive"
    bottom_polarity["Polarity Type"] = "Negative"

    # Combine the dataframes
    combined_df = pd.concat([top_polarity, bottom_polarity])

    # Visualisation as bar chart
    fig = px.bar(combined_df, y="main_artist", x="polarity", color="Polarity Type",
                 labels={"shortened_track_name": "Trackname",
                         "polarity": "Polarity", "main_artist": "Artist(s)"},
                 hover_data=["main_artist", "shortened_track_name"], color_discrete_map={
                     "Positive": "rgb(93, 105, 177, 0.5)",
                     "Negative": "rgb(229, 134, 6, 0.5)"
                 },
                 text="shortened_track_name")

    # Adjust the layout
    fig.update_layout(
        template="plotly_dark",
        showlegend=False,
        xaxis=dict(range=[-1, 1], dtick=0.5, title="Polarity"),
        yaxis=dict(title="Artist(s)", fixedrange=True, categoryorder='array',
                   categoryarray=combined_df['main_artist'].tolist()),
        autosize=True,
        margin=dict(l=150, r=80, t=80, b=80)
    )

    fig.update_traces(
        textfont=dict(family="Arial", size=16, color="white", weight="bold"),
        textposition="inside",
    )

    return fig


@app.callback(
    Output('polarity-graph', 'figure'),
    Input('year-dropdown', 'value')
)
def update_violin_plot(selected_year):
    # Filter the selcted year
    df_year = df[df['year_month'].str.startswith(selected_year)]

    # Convert numbers to monthnames
    month_mapping = {1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun",
                     7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"}

    # Replace the numbers with monthnames
    df_year['month_name'] = df_year['month'].map(month_mapping)

    # Visualize the data
    fig = px.violin(df_year, x='month_name', y='polarity', points=False,
                    labels={'month_name': 'Month', 'polarity': 'Polarity'})

    # Sort the monthnames
    fig.update_xaxes(categoryorder="array", categoryarray=["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                                                           "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])

    # Adjust the layout
    fig.update_layout(
        template='plotly_dark',
        yaxis=dict(range=[-1, 1], dtick=0.5),
        xaxis_title="Month"
    )

    return fig


@app.callback(
    Output('polarity-graph-top-50', 'figure'),
    Input('year-dropdown-top50', 'value')
)
def update_top50_scatter(selected_year):
    # Filter the selected year
    df_year = df[df['year'].astype(str) == selected_year]

    grouped_df = df_year.groupby('artist_names').agg(
        {'polarity': 'mean', 'duration_seconds': 'mean', 'max_days_on_chart': 'sum'}).reset_index()
    top_50_artists = grouped_df.nlargest(50, 'max_days_on_chart')

    fig = px.scatter(top_50_artists, x='polarity', y='duration_seconds', size='max_days_on_chart', color='artist_names',
                     hover_name='artist_names', labels={'polarity': 'Polarity (avg)', 'duration_seconds': 'Duration (avg in sec)', 'max_days_on_chart': 'Chart Days'})
    fig.update_layout(template='plotly_dark', showlegend=False, yaxis=dict(title="Duration (avg in sec)", range=[100, 350], dtick=50),
                      xaxis=dict(title="Polarity (avg)", range=[-0.75, 0.75], dtick=0.25))
    return fig


@app.callback(
    Output('polarity-graph-artist', 'figure'),
    Input('artist-dropdown', 'value')
)
def update_artist_polarity(selected_artists):
    # Get all rows which include one top 15 artist
    def match_artist(artist_names):
        return any(artist in [a.strip() for a in artist_names.split(',')] for artist in selected_artists)

    df_selected = df[df['artist_names'].apply(match_artist)]

    # Get the main artist (first one)
    def get_main_artist(artist_names):
        found_artists = [artist for artist in selected_artists if artist in [
            a.strip() for a in artist_names.split(',')]]
        if found_artists:
            return found_artists[0]
        return artist_names

    # Filter the main artist
    df_selected['main_artist'] = df_selected['artist_names'].apply(
        get_main_artist)

    polarity_by_month = df_selected.groupby(['year_month', 'main_artist'])[
        'polarity'].mean().reset_index()

    fig = px.line(polarity_by_month, x='year_month', y='polarity',
                  color='main_artist', labels={'year_month': 'Year', 'polarity': 'Polarity'})

    # Adjust the layout
    fig.update_layout(
        template='plotly_dark',
        yaxis=dict(range=[-1, 1], dtick=0.5, fixedrange=True),
        legend_title="Artist(s)",
        xaxis=dict(showgrid=True, fixedrange=True, title="Year"),
        xaxis_title="Year",
        yaxis_title="Polarity",
        autosize=True,
        margin=dict(l=80, r=80, t=80, b=80)
    )

    fig.update_yaxes(categoryorder='array', categoryarray=selected_artists)

    return fig
