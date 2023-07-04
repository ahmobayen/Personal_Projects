# Libraries
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px

from Model import DBConnection

# variables
count = 0
result = []
dataFrame = {
    'date': [],
    'value': [],
    'polarity': []
}
column = []

# Getting data
try:
    query = 'select date, polarity, count(value) from socialmedia.data_nlp_processed group by date,polarity order by date'
    result = DBConnection.execute_query(query)

    for row in result:
        dataFrame['date'].append(row[0])
        dataFrame['polarity'].append(row[1])
        dataFrame['value'].append(row[2])
except:
    pass
finally:
    df = pd.DataFrame(dataFrame)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

try:
    fig = px.line(df, x='date', y='value', color='polarity', title='Comments Activity')

    app.layout = html.Div(children=[
        html.H1(children='Hello Dash'),

        html.Div(children=''' Dash: A web application framework for Python.'''),

        dcc.Graph(
            id='example-graph',
            figure=fig
        )
    ])

    if __name__ == '__main__':
        app.run_server(debug=True)
except:
    raise Exception()
