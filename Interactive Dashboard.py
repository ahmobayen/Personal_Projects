import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Load data
spacex_df = pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv")

# Initialize the Dash app
app = dash.Dash(__name__)
server = app.server

# Unique launch sites for dropdown options
launch_sites = spacex_df['Launch Site'].unique()
site_options = [{'label': site, 'value': site} for site in launch_sites]
site_options.insert(0, {'label': 'All Sites', 'value': 'All Sites'})

# App layout
app.layout = html.Div([
    html.H1('SpaceX Launch Records Dashboard', style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
    dcc.Dropdown(id='site_dropdown', options=site_options, placeholder='Select a Launch Site here', searchable=True, value='All Sites'),
    html.Br(),
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),
    html.P("Payload range (Kg):"),
    dcc.RangeSlider(
        id='payload_slider',
        min=0,
        max=10000,
        step=1000,
        marks={i: f'{i} kg' for i in range(0, 11000, 1000)},
        value=[spacex_df['Payload Mass (kg)'].min(), spacex_df['Payload Mass (kg)'].max()]
    ),
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])

# Callbacks
@app.callback(
    Output('success-pie-chart', 'figure'),
    [Input('site_dropdown', 'value')]
)
def update_pie_chart(site_dropdown):
    if site_dropdown == 'All Sites':
        df = spacex_df
        title = 'Total Success Launches By all sites'
    else:
        df = spacex_df[spacex_df['Launch Site'] == site_dropdown]
        title = f'Total Success Launches for site {site_dropdown}'
    success_counts = df[df['class'] == 1]['Launch Site'].value_counts()
    fig = px.pie(names=success_counts.index, values=success_counts.values, title=title, hole=0.3)
    return fig

@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [Input('site_dropdown', 'value'),
     Input('payload_slider', 'value')]
)
def update_scatter_chart(site_dropdown, payload_slider):
    low, high = payload_slider
    if site_dropdown == 'All Sites':
        df = spacex_df[(spacex_df['Payload Mass (kg)'] >= low) & (spacex_df['Payload Mass (kg)'] <= high)]
        title = 'Payload Success Scatter Chart for All Sites'
    else:
        df = spacex_df[(spacex_df['Payload Mass (kg)'] >= low) & (spacex_df['Payload Mass (kg)'] <= high) & (spacex_df['Launch Site'] == site_dropdown)]
        title = f'Payload Success Scatter Chart for {site_dropdown}'
    fig = px.scatter(df, x='Payload Mass (kg)', y='class', color='Booster Version', size='Payload Mass (kg)',
                     hover_data=['Payload Mass (kg)'], title=title)
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
