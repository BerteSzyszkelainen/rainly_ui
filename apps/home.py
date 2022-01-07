import pytz
from dash import dcc
from dash import html
from datetime import datetime
from dash.dependencies import Input, Output
from babel.dates import format_datetime

from app import app

layout = html.Div(
    id="root-div-welcome",
    children=[
        html.Div(
            id="div-timer",
            children=html.Label(id='label-timer-home-page')
        ),
        html.Div(
            id="div-navigation",
            children=[
                dcc.Link(id='home', className="active", children='Start', href='/'),
                dcc.Link(id='home', children='Dzienna analiza', href='/apps/daily'),
                dcc.Link(id='home', children='Miesięczna analiza', href='/apps/monthly'),
                dcc.Link(id='home', children='Roczna analiza', href='/apps/yearly')
            ]
        ),
        html.Div(
            id="div-welcome",
            children=html.Label(id='label-welcome', children="Witaj w Rainly!")
        ),
        dcc.Interval(
            id='interval-timer',
            interval=1 * 1000,
            n_intervals=0
        )
])


@app.callback(
    Output('label-timer-home-page', 'children'),
    Input('interval-timer', 'n_intervals')
)
def update_timer(n):
    return format_datetime(datetime.now(pytz.timezone('Europe/Warsaw')), format="EEEE, d MMMM yyyy, HH:mm:ss", locale='pl')
