import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import dash_table
from dash.exceptions import PreventUpdate
import flask
from flask import Flask
import pandas as pd
import dateutil.relativedelta
from datetime import date
import datetime
import requests, pickle, base64
import numpy as np
import plotly
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dash_utils import make_card, ticker_inputs
#instantiate dash app server using flask for easier hosting
server = Flask(__name__)
app = dash.Dash(__name__,server = server ,meta_tags=[{ "content": "width=device-width"}], external_stylesheets=[dbc.themes.BOOTSTRAP])

#used for dynamic callbacks
app.config.suppress_callback_exceptions = True

layout1 = html.Div([
dbc.Row([dbc.Col(make_card("Enter Ticker", "success", ticker_inputs('ticker-input', 'date-picker', 36)))]) #row 1
,html.Div([
    html.Div([dcc.Graph(id="GDP-chart")],className='col-sm-3'),
    html.Div([dcc.Graph(id="PMI-chart")],className='col-sm-3'),
    html.Div([dcc.Graph(id="Inflation-chart")],className='col-sm-3'),
    html.Div([dcc.Graph(id="CC-chart")],className='col-sm-3')
    

    ], className='row'
    )
,html.Div([
    html.Div([dcc.Graph(id="Interest-chart")],className='col-sm-3'),
    html.Div([dcc.Graph(id="Currency-chart")],className='col-sm-3'),
    html.Div([dcc.Graph(id="Unemployment-chart")],className='col-sm-3'),
    html.Div([dcc.Graph(id="Stocks-chart")],className='col-sm-3')
    

    ], className='row'
    )    
#,dbc.Row(dbc.Col([make_card("Fin table ", "secondary", html.Div(id="fin-table"))]))
,dbc.Row(dbc.Col([make_card("News table ", "secondary", html.Div(id="news-table"))]))
#,dcc.Graph(id="sentiment-chart")
,dbc.Row(dbc.Col([make_card("COT table ", "secondary", html.Div(id="COT-table"))]))
,dcc.Graph(id="cot-line-chart")


],className='col') #end div
app.layout= layout1
app.title = 'FUNDAMENTOS!!'
'''
@app.callback(Output('fin-table', 'children'),
[Input('ticker-input', 'value')])
def fin_report(sym):
    string = requests.post('http://127.0.0.1:5001/fin_reports', json={'symbol':sym})
    #print(string.text)
    df = pickle.loads(base64.b64decode(string.text))
    #print(df)
    table = dbc.Table.from_dataframe(df, striped=True
            , bordered=True, style={'textAlign': 'center'}, hover=True)
    return table
'''
@app.callback(Output('news-table', 'children'),
[Input('ticker-input', 'value')])
def news_report(sym):
    string = requests.post('http://127.0.0.1:5001/news', json={'symbol':sym, 'days': 5})
    df = pickle.loads(base64.b64decode(string.text))
    df['date']= df['date'].dt.strftime('%m-%d-%Y')
    table = dbc.Table.from_dataframe(df, striped=True
            , bordered=True, hover=True, style={'textAlign': 'center'})
    return table

@app.callback(Output('COT-table', 'children'),
[Input('ticker-input', 'value')])
def cot_report(sym):
    string = requests.post('http://127.0.0.1:5001/cot', json={'symbol':sym, 'number': -12})
    df = pickle.loads(base64.b64decode(string.text))
    df = df.reset_index()
    df.columns.values[0] = 'Date'
    #df['Date'] = pd.to_datetime(df['Date']
    df['Date']= df['Date'].dt.strftime('%m-%d-%Y')
    table = dbc.Table.from_dataframe(df, striped=True, style={'textAlign': 'center'},
             bordered=True, hover=True)
    return table

@app.callback(
    Output("cot-line-chart", "figure"),
    [Input("ticker-input", "value")])
def update_line_chart(sym):
    string = requests.post('http://127.0.0.1:5001/cot', json={'symbol':sym, 'number': -12})
    df = pickle.loads(base64.b64decode(string.text))
    fig = px.line(df, title='COT for '+sym+' currency')
    return fig

@app.callback(
    Output("GDP-chart", "figure"),
    [Input("ticker-input", "value")])
def update_line_chartg(sym):
    string = requests.post('http://127.0.0.1:5001/econ_data', json={'symbol':sym, 'number': -12})
    df = pickle.loads(base64.b64decode(string.text))
    sm = df['GDP'].dropna()
    fig = px.line(sm, title='GDP annualized % for '+sym)
    fig.update_layout(showlegend=False)
    return fig

@app.callback(
    Output("CC-chart", "figure"),
    [Input("ticker-input", "value")])
def update_line_chartcc(sym):
    string = requests.post('http://127.0.0.1:5001/econ_data', json={'symbol':sym, 'number': -12})
    df = pickle.loads(base64.b64decode(string.text))
    sm = df['CC'].dropna()
    fig = px.line(sm, title='Consumer Confidence for '+sym)
    fig.update_layout(showlegend=False)
    return fig

@app.callback(
    Output("PMI-chart", "figure"),
    [Input("ticker-input", "value")])
def update_line_chartpm(sym):
    string = requests.post('http://127.0.0.1:5001/econ_data', json={'symbol':sym, 'number': -12})
    df = pickle.loads(base64.b64decode(string.text))
    sm = df['PMI'].dropna()
    fig = px.line(sm, title='PMI for '+sym)
    fig.update_layout(showlegend=False)
    return fig

@app.callback(
    Output("Inflation-chart", "figure"),
    [Input("ticker-input", "value")])
def update_line_chartin(sym):
    string = requests.post('http://127.0.0.1:5001/econ_data', json={'symbol':sym, 'number': -12})
    df = pickle.loads(base64.b64decode(string.text))
    sm = df['Inflation'].dropna()
    fig = px.line(sm, title='Inflation annualized % for '+sym)
    fig.update_layout(showlegend=False)
    return fig

@app.callback(
    Output("Interest-chart", "figure"),
    [Input("ticker-input", "value")])
def update_line_chartint(sym):
    string = requests.post('http://127.0.0.1:5001/econ_data', json={'symbol':sym, 'number': -12})
    df = pickle.loads(base64.b64decode(string.text))
    sm = df['Interest Rate'].dropna()
    fig = px.line(sm, title='Interest rates % for '+sym)
    fig.update_layout(showlegend=False)
    return fig

@app.callback(
    Output("Currency-chart", "figure"),
    [Input("ticker-input", "value")])
def update_line_chartcu(sym):
    string = requests.post('http://127.0.0.1:5001/econ_data', json={'symbol':sym, 'number': -12})
    df = pickle.loads(base64.b64decode(string.text))
    sm = df['Currency (USD)'].dropna()
    fig = px.line(sm, title='Currency exchange (USD) for'+sym)
    fig.update_layout(showlegend=False)
    return fig

@app.callback(
    Output("Unemployment-chart", "figure"),
    [Input("ticker-input", "value")])
def update_line_chartun(sym):
    string = requests.post('http://127.0.0.1:5001/econ_data', json={'symbol':sym, 'number': -12})
    df = pickle.loads(base64.b64decode(string.text))
    sm = df['Unemployment'].dropna()
    fig = px.line(sm, title='Unemployment % for '+sym)
    fig.update_layout(showlegend=False)
    return fig

@app.callback(
    Output("Stocks-chart", "figure"),
    [Input("ticker-input", "value")])
def update_line_chartin(sym):
    string = requests.post('http://127.0.0.1:5001/econ_data', json={'symbol':sym, 'number': -12})
    df = pickle.loads(base64.b64decode(string.text))
    sm = df['Stock Market'].dropna()
    fig = px.line(sm, title='Normalized Stock Index for '+sym)
    fig.update_layout(showlegend=False)
    return fig


@app.callback(
    Output("sentiment-chart", "figure"),
    [Input("ticker-input", "value")])
def update_line_chart(sym):
    string = requests.post('http://127.0.0.1:5001/news', json={'symbol':sym, 'days': 100})
    df = pickle.loads(base64.b64decode(string.text))
    a = df['SMA_30'].to_numpy()
    df['SMA_30'] = a[::-1]
    fig = px.line(df['SMA_30'], title='Sentiment Moving Average 30-Posts')
    return fig
#API KEY p9phc4wqs4FbiD071fe5Ow0z0

#API SECRET QpkXhbfaRzcIqa5YokvuBs3EXDHRk44je6uA42NbuYbLZsID7W

#Bearer toekn AAAAAAAAAAAAAAAAAAAAAONgIQEAAAAAYYdXmXB3GKzVIVxD1s4da%2Fi8%2F5g%3DhkV9NSIRIbYmIh6lMgAo6e8OjCjj2WEhv4sB5JTeNkVxBgIGET
if __name__ == '__main__':
    app.run_server(debug=True)
