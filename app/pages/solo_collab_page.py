from dash import html, dcc, Input, Output
import plotly.express as px
import pandas as pd
from app.app import app
from pathlib import Path

csv_path = Path(__file__).resolve(
).parents[2] / 'data' / 'cleaned_global_17-24_Spotify.csv'
df = pd.read_csv(csv_path)

colab_counts = df['is_colab'].value_counts().reset_index()
colab_counts.columns = ['is_colab', 'count']

pie_colab = px.pie(
    colab_counts,
    names='is_colab',
    values='count',
    title="Collaboration Count Breakdown",
    color_discrete_sequence=px.colors.qualitative.Vivid
)

pie_colab.update_traces(textinfo='percent+label')
pie_colab.update_layout(template="plotly_dark",                         autosize=False,
                        width=900,
                        height=400,)

layout = html.Div([
    html.Div([

        html.Div([
            html.P("Lorem ipsum dolor sit amet, consectetur adipiscing elit. ")
        ], className='t1_colab'),
        html.Iframe(src="/assets/artist_collab_network.html",
                    className='graph_colab',  width="100%", height="800px"),
        dcc.Graph(figure=pie_colab, className='pie_colab'),
        html.Div([
            html.P("Lorem ipsum dolor sit amet, consectetur adipiscing elit. ")
        ], className='t2_colab'),
        dcc.Dropdown(
            id='metric-dropdown',
            options=[
                {'label': 'Median Total Streams', 'value': 'total_streams'},
                {'label': 'Max Days on Chart', 'value': 'max_days_on_chart'},
                {'label': 'Min Peak Rank', 'value': 'min_peak_rank'}
            ],
            value='total_streams',
            clearable=False,
            className='dropdown dropdown_colab'
        ),

        dcc.Graph(id='bar_colab', className='bar_colab'),

        html.Div([
            html.P("Lorem ipsum dolor sit amet, consectetur adipiscing elit. ")
        ], className='t3_colab')

    ], className='container_colab')
])


@app.callback(
    Output('bar_colab', 'figure'),
    [Input('metric-dropdown', 'value')]
)
def update_bar_chart(selected_metric):
    metric_label = {
        'total_streams': 'Median Total Streams',
        'max_days_on_chart': 'Median Max Days on Chart',
        'min_peak_rank': 'Median Min Peak Rank'
    }

    grouped_data = df.groupby('is_colab')[
        selected_metric].median().reset_index()

    fig = px.bar(
        grouped_data,
        x='is_colab',
        y=selected_metric,
        title=f"{metric_label[selected_metric]} by Collaboration Status",
        labels={'is_colab': 'Collaboration',
                selected_metric: metric_label[selected_metric]},
        color='is_colab',
        color_discrete_sequence=px.colors.qualitative.Vivid
    )

    fig.update_layout(
        xaxis_title="Collaboration",
        yaxis_title=metric_label[selected_metric],
        template="plotly_dark"
    )

    return fig
