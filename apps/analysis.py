import pytz
from dash import dcc
from dash import html
from datetime import datetime
from dash.dependencies import Input, Output
from babel.dates import format_datetime

from app import app

layout = html.Div(
    id="root-div",
    children=[
        html.Div(
            id="div-timer",
            children=html.Label(id='label-timer-analysis')
        ),
        html.Div(
            id="div-navigation",
            children=[
                dcc.Link(id='home', children='Start', href='/'),
                dcc.Link(id='home', children='Opady', href='/apps/rainfall'),
                dcc.Link(id='home', children='Temperatura', href='/apps/temperature'),
                dcc.Link(id='home', children='Wilgotność', href='/apps/humidity'),
                dcc.Link(id='home', children='Ciśnienie', href='/apps/pressure'),
                dcc.Link(id='home', children='Wiatr', href='/apps/wind'),
                dcc.Link(id='home', className="active", children='Moduł analityczny', href='/apps/analysis'),
            ]
        ),
        html.Div(
            id="div-info",
            children=html.Label(id='label-info', children="W budowie:)")
        ),
        dcc.Interval(
            id='interval-timer',
            interval=1 * 1000,
            n_intervals=0
        )
])


@app.callback(
    Output('label-timer-analysis', 'children'),
    Input('interval-timer', 'n_intervals')
)
def update_timer(n):
    return format_datetime(datetime.now(pytz.timezone('Europe/Warsaw')), format="EEE, d MMMM yyyy, HH:mm:ss", locale='pl')
