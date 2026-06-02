import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px
from io import StringIO
import base64

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Upload(
        id='upload-data',
        multiple=False,
        children=html.Button(
            'Click to Upload files',
            
    )),
    
    dcc.Dropdown(
        id='chart-type',
        options=[
            {'label': 'Bar Chart', 'value': 'bar'},
            {'label': 'Line Chart', 'value': 'line'}
        ]),

    dcc.Graph(id='vizout')
])


@app.callback(Output('vizout', 'figure'),
              Input('upload-data', 'contents'),
              Input('chart-type', 'value'))

def update_output(contents, chart_type):
    if contents is None:
        return px.scatter(title='Please upload a file')
    
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    df = pd.read_csv(StringIO(decoded.decode('utf-8')))


    if chart_type == 'Bar':
        fig = px.bar(df, x=df.columns[0], y=df.columns[5], title='Bar Chart')
    elif chart_type == 'Line':
        fig = px.line(df, x=df.columns[0], y=df.columns[5], title='Line Chart')
    else:
        fig = px.scatter(df, x=df.columns[0], y=df.columns[5], title='Line Chart')
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)