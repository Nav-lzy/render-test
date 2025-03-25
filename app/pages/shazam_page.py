from dash import html, dcc, Input, Output
import plotly.express as px
import pandas as pd
from pathlib import Path

# Load the Spotify data
csv_path = Path(__file__).resolve(
).parents[2] / 'data' / 'raw_data' / 'daily_global_charts/daily_combined/daily17-24.csv'
df = pd.read_csv(csv_path)

# Process date info
df["date"] = pd.to_datetime(df["date"])
df_grouped = df.groupby("date")["streams"].sum().reset_index()
df_grouped["month"] = df_grouped["date"].dt.month
df_grouped["month_name"] = df_grouped["date"].dt.strftime("%B")
df_grouped["weekday"] = df_grouped["date"].dt.weekday
df_grouped["weekday_name"] = df_grouped["date"].dt.strftime("%A")

# Load COVID data
csv_path = Path(__file__).resolve(
).parents[2] / 'data' / 'WHO-COVID-19-global-daily-data.csv'
covid = pd.read_csv(csv_path)
covid["Date_reported"] = pd.to_datetime(covid["Date_reported"])
covid_grouped = covid.groupby("Date_reported")["New_cases"].sum().reset_index()

# Merge data
merged_df = pd.merge(covid_grouped, df_grouped,
                     left_on="Date_reported", right_on="date", how="inner")
bin_edges = [-1e11, 1000, 5000, 10000, 50000, 100000, 500000, float('inf')]
bin_labels = ["0-1000", "1000-5000", "5000-10000",
              "10000-50000", "50000-100000", "100000-500000", "500000+"]
merged_df['New_cases_binned'] = pd.cut(
    merged_df['New_cases'], bins=bin_edges, labels=bin_labels)

# Bar chart: Median daily streams per weekday
df_weekday = merged_df.groupby(["weekday", "weekday_name"])[
    "streams"].median().reset_index()
df_weekday = df_weekday.sort_values(by="weekday")

bar_covid_week = px.bar(
    df_weekday,
    x="weekday_name",
    y="streams",
    title="Median Daily Streams Per Weekday",
    labels={"weekday_name": "Weekday", "streams": "Median Streams"},
    text_auto=True,
    color="weekday_name",
    color_discrete_sequence=px.colors.qualitative.Vivid
)
bar_covid_week.update_layout(
    template="plotly_dark",
    xaxis_title="Day of the Week",
    yaxis_title="Total Streams"
)

# Bar chart: Median daily streams per month
df_month = merged_df.groupby(["month", "month_name"])[
    "streams"].median().reset_index()
df_month = df_month.sort_values(by="month")

bar_covid_month = px.bar(
    df_month,
    x="month_name",
    y="streams",
    title="Median Daily Streams Per Month",
    labels={"month_name": "Month", "streams": "Median Streams"},
    text_auto=True,
    color="month_name",
    color_discrete_sequence=px.colors.qualitative.Vivid
)
bar_covid_month.update_layout(
    template="plotly_dark",
    xaxis_title="Month",
    yaxis_title="Total Streams"
)

# Box plot: Streams distribution based on COVID-19 case intervals
boxplot_covid = px.box(
    merged_df,
    x="New_cases_binned",
    y="streams",
    title="Streams Distribution Based on COVID-19 Case Intervalls",
    labels={"New_cases_binned": "Intervalls of COVID-19 Cases",
            "streams": "Streams"},
    color="New_cases_binned",
    color_discrete_sequence=px.colors.qualitative.Vivid,
    category_orders={"New_cases_binned": bin_labels}
)
boxplot_covid.update_layout(
    xaxis_tickangle=-45,
    template="plotly_dark"
)

# Scatter plot: Weekly average streams vs COVID cases
merged_df['streams_7day_avg'] = merged_df['streams'].rolling(window=7).mean()
merged_df['Week'] = merged_df['Date_reported'].dt.to_period('W').dt.start_time
merged_df = merged_df[merged_df['New_cases'] >= 0]
merged_df['size_scaled'] = merged_df['New_cases'] + 500000

scatter_covid = px.scatter(
    merged_df,
    x='Week',
    y='streams_7day_avg',
    size='size_scaled',
    color='New_cases',
    title="Streams With Weekly Streams and COVID Cases",
    labels={
        "streams_7day_avg": "Weekly Average of Streams",
        "Week": "Week",
        "New_cases": "COVID Cases"
    },
    color_continuous_scale=px.colors.sequential.YlOrRd
)
scatter_covid.update_layout(
    template="plotly_dark",
    xaxis_title="Week",
    yaxis_title="Weekly Average of Streams",
    legend_title="COVID cases",
    coloraxis=dict(cmin=0, cmax=500000)
)

# Final layout with all graphs
layout = html.Div([
    dcc.Location(id='url', refresh=False),
    dcc.Graph(figure=bar_covid_week, className='bar_covid_week'),
    html.Div([
        html.P("Lorem ipsum dolor sit amet, consectetur adipiscing elit. ")
    ], className='t1_covid'),
    dcc.Graph(figure=bar_covid_month, className='bar_covid_month'),
    html.Div([
        html.P("Lorem ipsum dolor sit amet, consectetur adipiscing elit. ")
    ], className='t2_covid'),
    dcc.Graph(figure=boxplot_covid, className='boxplot_covid'),
    html.Div([
        html.P("Lorem ipsum dolor sit amet, consectetur adipiscing elit. ")
    ], className='t3_covid'),
    dcc.Graph(figure=scatter_covid, className='scatter_covid'),
    html.Div([
        html.P("Lorem ipsum dolor sit amet, consectetur adipiscing elit. ")
    ], className='t4_covid'),
], className='container_covid')
