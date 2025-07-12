# Funnel Drop-Off Analysis Dashboard using Plotly Dash

import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px

# Load dataset
df = pd.read_csv("funnel_dropoff_dataset.csv")
df['signup_date'] = pd.to_datetime(df['signup_date'])

# Initialize Dash app
app = dash.Dash(__name__)
app.title = "Funnel Drop-Off Dashboard"

# Layout
app.layout = html.Div([
    html.H1("User Funnel Drop-Off Analysis", style={"textAlign": "center"}),

    html.Div([
        html.Div([
            html.Label("Device Type"),
            dcc.Dropdown(
                options=[{"label": dev, "value": dev} for dev in df['device_type'].unique()],
                value=None,
                id='device-filter',
                placeholder="Select a device type",
                multi=True
            )
        ], style={"width": "30%", "display": "inline-block", "padding": "10px"}),

        html.Div([
            html.Label("Channel"),
            dcc.Dropdown(
                options=[{"label": ch, "value": ch} for ch in df['channel'].unique()],
                value=None,
                id='channel-filter',
                placeholder="Select acquisition channel",
                multi=True
            )
        ], style={"width": "30%", "display": "inline-block", "padding": "10px"}),

        html.Div([
            html.Label("Signup Date Range"),
            dcc.DatePickerRange(
                id='date-range',
                min_date_allowed=df['signup_date'].min(),
                max_date_allowed=df['signup_date'].max(),
                start_date=df['signup_date'].min(),
                end_date=df['signup_date'].max()
            )
        ], style={"width": "35%", "display": "inline-block", "padding": "10px"})
    ]),

    html.Br(),

    html.Div(id='kpi-banner', style={"textAlign": "center", "fontSize": "20px", "padding": "10px", "backgroundColor": "#f0f0f0"}),

    dcc.Graph(id='funnel-bar-chart'),
    html.Div(id='dropoff-table', style={"padding": "20px", "fontSize": "18px"}),

    html.Br(),
    html.H2("Heatmap: CTR by Device and Channel", style={"textAlign": "center"}),
    dcc.Graph(id='heatmap-chart')
])

# Callbacks to update charts and table
@app.callback(
    [Output('funnel-bar-chart', 'figure'),
     Output('dropoff-table', 'children'),
     Output('heatmap-chart', 'figure'),
     Output('kpi-banner', 'children')],
    [Input('device-filter', 'value'),
     Input('channel-filter', 'value'),
     Input('date-range', 'start_date'),
     Input('date-range', 'end_date')]
)
def update_dashboard(devices, channels, start_date, end_date):
    dff = df.copy()
    if devices:
        dff = dff[dff['device_type'].isin(devices)]
    if channels:
        dff = dff[dff['channel'].isin(channels)]
    dff = dff[(dff['signup_date'] >= pd.to_datetime(start_date)) & (dff['signup_date'] <= pd.to_datetime(end_date))]

    stages = ['step_1_landing', 'step_2_account_created', 'step_3_email_verified',
              'step_4_first_use', 'step_5_engaged_return']

    stage_counts = [dff[stage].sum() for stage in stages]
    stage_names = ['Landing', 'Account Created', 'Email Verified', 'First Use', 'Engaged Return']

    # Create funnel chart
    funnel_fig = px.bar(
        x=stage_names,
        y=stage_counts,
        labels={'x': 'Funnel Stage', 'y': 'User Count'},
        title="User Count per Funnel Stage"
    )

    # Drop-off table
    dropoffs = []
    for i in range(len(stage_counts)-1):
        loss = stage_counts[i] - stage_counts[i+1]
        pct_loss = (loss / stage_counts[i]) * 100 if stage_counts[i] > 0 else 0
        dropoffs.append(f"Drop from {stage_names[i]} to {stage_names[i+1]}: {loss} users ({pct_loss:.1f}%)")

    # Heatmap data
    heatmap_df = dff.groupby(['device_type', 'channel']).agg(
        impressions=('step_1_landing', 'count'),
        engaged=('step_5_engaged_return', 'sum')
    ).reset_index()
    heatmap_df['ctr'] = heatmap_df['engaged'] / heatmap_df['impressions']

    heatmap_fig = px.density_heatmap(
        heatmap_df,
        x='channel',
        y='device_type',
        z='ctr',
        color_continuous_scale='Blues',
        title='CTR Heatmap by Device and Channel',
        labels={'ctr': 'CTR'}
    )

    total_users = len(dff)
    total_engaged = dff['step_5_engaged_return'].sum()
    total_ctr = (total_engaged / total_users) * 100 if total_users > 0 else 0
    kpi_banner = f"Total Users: {total_users:,} | Engaged Users: {total_engaged:,} | Engagement CTR: {total_ctr:.2f}%"

    return funnel_fig, html.Ul([html.Li(d) for d in dropoffs]), heatmap_fig, kpi_banner

# Run app
if __name__ == '__main__':
    app.run_server(debug=True)
