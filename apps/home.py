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
            children=html.Label(id='label-timer-home-page')
        ),
        html.Div(
            id="div-navigation",
            children=[
                dcc.Link(id='home', className="active", children='Start', href='/'),
                dcc.Link(id='home', children='Godzinowa analiza', href='/apps/hourly'),
                dcc.Link(id='home', children='Dzienna analiza', href='/apps/daily'),
                dcc.Link(id='home', children='Miesięczna analiza', href='/apps/monthly')
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
    return format_datetime(datetime.now(), format="EEEE, dd MMM yyyy, HH:mm:ss", locale='pl')