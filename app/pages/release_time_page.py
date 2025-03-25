from dash import html, dcc, Input, Output
import plotly.express as px
import pandas as pd
from app import app
from pathlib import Path


csv_path = Path(__file__).resolve(
).parents[2] / 'data' / 'cleaned_global_17-24_Spotify.csv'

df = pd.read_csv(csv_path)

bin_counts = df['relase-chart_days_bins'].value_counts().reindex(
    ['0 days', '<1 week', '1-2 weeks', '2-3 weeks', '3-4 weeks', '4+ weeks']
)

pie_release = px.pie(
    names=bin_counts.index,
    values=bin_counts.values,
    title='Track Counts per Release - Chart Interval',
    color=bin_counts.index,
    color_discrete_sequence=px.colors.qualitative.Vivid
)

pie_release.update_traces(textinfo='percent+label')
pie_release.update_layout(template="plotly_dark",
                          autosize=False,
                          width=900,
                          height=400,
                          )

mean_values = df.groupby('relase-chart_days_bins')[
    ['max_days_on_chart', 'total_streams', 'min_peak_rank']
].mean().reindex(['0 days', '<1 week', '1-2 weeks', '2-3 weeks', '3-4 weeks', '4+ weeks'])

overall_means = df[['max_days_on_chart',
                    'total_streams', 'min_peak_rank']].mean()

bar_release = px.bar(
    x=mean_values.index,
    y=mean_values['max_days_on_chart'],
    text=mean_values['max_days_on_chart'].round(1),
    labels={'x': 'Time Baskets', 'y': 'Average Max Days on Chart'},
    title='Average Max Days on Chart per Time Interval',
    color=mean_values.index,
    color_discrete_sequence=px.colors.qualitative.Vivid
)

bar_release.add_hline(
    y=overall_means['max_days_on_chart'],
    line_dash="dash",
    line_color="red",
    annotation_text=f"Overall Mean: {overall_means['max_days_on_chart']:.1f}",
    annotation_position="top left"
)

bar_release.update_traces(textposition='outside')
bar_release.update_layout(
    xaxis_title="Time Baskets",
    yaxis_title="Average Max Days on Chart",
    template="plotly_dark"
)

violin_release = px.violin(
    df,
    x='relase-chart_days_bins',
    y='max_days_on_chart',
    box=True,
    points='all',
    color='relase-chart_days_bins',
    color_discrete_sequence=px.colors.qualitative.Vivid,
    title='Distribution of Max Days on Chart per Time Interval',
)

overall_median = df['max_days_on_chart'].median()
violin_release.add_hline(
    y=overall_median,
    line_dash="dash",
    line_color="red",
    annotation_text=f"Overall Median: {overall_median:.1f}",
    annotation_position="top left"
)

violin_release.update_layout(
    xaxis_title="Time Baskets",
    yaxis_title="Max Days on Chart",
    yaxis=dict(range=[0, 200]),
    template="plotly_dark",
)

dropdown = dcc.Dropdown(
    id='metric-dropdown',
    options=[
        {'label': 'Max Days on Chart', 'value': 'max_days_on_chart'},
        {'label': 'Total Streams', 'value': 'total_streams'},
        {'label': 'Rank', 'value': 'min_peak_rank'},
    ], className='dropdown',
    value='max_days_on_chart'
)


@app.callback(
    Output('bar-release', 'figure'),
    [Input('metric-dropdown', 'value')]
)
def update_bar_release(selected_metric):
    updated_bar_release = px.bar(
        x=mean_values.index,
        y=mean_values[selected_metric],
        text=mean_values[selected_metric].round(1),
        labels={'x': 'Time Baskets',
                'y': f'Average {selected_metric.replace("_", " ").title()}'},
        title=f'Average {selected_metric.replace("_", " ").title()} per Time Interval',
        color=mean_values.index,
        color_discrete_sequence=px.colors.qualitative.Vivid
    )

    updated_bar_release.add_hline(
        y=overall_means[selected_metric],
        line_dash="dash",
        line_color="red",
        annotation_text=f"Overall Mean: {overall_means[selected_metric]:.1f}",
        annotation_position="top left"
    )

    updated_bar_release.update_traces(textposition='outside')
    updated_bar_release.update_layout(
        xaxis_title="Time Baskets",
        yaxis_title=f"Average {selected_metric.replace('_', ' ').title()}",
        template="plotly_dark"
    )

    return updated_bar_release


layout = html.Div([
    html.Div([
        dcc.Graph(figure=pie_release, className='pie-release',
                  config={"responsive": True}),

        html.Div([
            html.P("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Quisque placerat lectus urna, a convallis sapien viverra ut. Sed vitae metus sit amet felis ornare consequat in a leo. Nulla facilisi. Etiam feugiat, neque bibendum feugiat commodo, velit odio posuere mi, vel egestas odio sapien ut urna. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Aliquam vitae cursus nibh. Vestibulum convallis felis mollis feugiat ultrices. Etiam semper pretium mi. Quisque consequat neque et auctor volutpat. Donec pellentesque ante id arcu finibus, in elementum massa feugiat. Nullam consequat felis quis nunc lobortis finibus. Vivamus ultrices facilisis pharetra. Sed non malesuada purus, at porttitor massa. Donec iaculis faucibus vestibulum. Curabitur pulvinar placerat suscipit. Sed fermentum sapien pulvinar, tristique lacus at, vestibulum nisi.")
        ], className='t1-release'),

        html.Div([
            html.P("After Pie Chart")
        ], className='t2-release'),

        dropdown,
        dcc.Graph(id='bar-release', figure=bar_release,
                  className='bar-release'),

        html.Div([
            html.P("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Quisque placerat lectus urna, a convallis sapien viverra ut. Sed vitae metus sit amet felis ornare consequat in a leo. Nulla facilisi. Etiam feugiat, neque bibendum feugiat commodo, velit odio posuere mi, vel egestas odio sapien ut urna. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Aliquam vitae cursus nibh. Vestibulum convallis felis mollis feugiat ultrices. Etiam semper pretium mi. Quisque consequat neque et auctor volutpat. Donec pellentesque ante id arcu finibus, in elementum massa feugiat. Nullam consequat felis quis nunc lobortis finibus. Vivamus ultrices facilisis pharetra. Sed non malesuada purus, at porttitor massa. Donec iaculis faucibus vestibulum. Curabitur pulvinar placerat suscipit. Sed fermentum sapien pulvinar, tristique lacus at, vestibulum nisi.")
        ], className='t3-release'),

        dcc.Graph(figure=violin_release, className='violin-release'),

        html.Div([
            html.P("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Quisque placerat lectus urna, a convallis sapien viverra ut. Sed vitae metus sit amet felis ornare consequat in a leo. Nulla facilisi. Etiam feugiat, neque bibendum feugiat commodo, velit odio posuere mi, vel egestas odio sapien ut urna. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Aliquam vitae cursus nibh. Vestibulum convallis felis mollis feugiat ultrices. Etiam semper pretium mi. Quisque consequat neque et auctor volutpat. Donec pellentesque ante id arcu finibus, in elementum massa feugiat. Nullam consequat felis quis nunc lobortis finibus. Vivamus ultrices facilisis pharetra. Sed non malesuada purus, at porttitor massa. Donec iaculis faucibus vestibulum. Curabitur pulvinar placerat suscipit. Sed fermentum sapien pulvinar, tristique lacus at, vestibulum nisi.")
        ], className='t4-release')

    ], className='container-release')
])
