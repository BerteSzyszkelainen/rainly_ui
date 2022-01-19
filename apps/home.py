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
            children=html.Label(id='label-timer-home')
        ),
        html.Div(
            id="div-navigation",
            children=[
                dcc.Link(id='home', className="active", children='Start', href='/'),
                dcc.Link(id='home', children='Opady', href='/apps/rainfall'),
                dcc.Link(id='home', children='Temperatura', href='/apps/temperature'),
                dcc.Link(id='home', children='Wilgotność', href='/apps/humidity'),
                dcc.Link(id='home', children='Ciśnienie', href='/apps/pressure'),
                dcc.Link(id='home', children='Wiatr', href='/apps/wind'),
                dcc.Link(id='home', children='Moduł analityczny', href='/apps/analysis'),
            ]
        ),
        html.Div(
            id="div-welcome",
            children=html.Label(id='label-welcome', children="Witaj w Rainly!")
        ),
        html.Div(
            id="div-current-measurements",
            children=html.Div(id="div-current-measurements-row", children=
            [html.Div(
                      id="div-current-temperature-home-page",
                      children=html.Label(id='label-current-temperature-home-page', children="2 °C")
                      ),
                      html.Div(
                          id="div-current-humidity-home-page",
                          children=html.Label(id='label-current-humidity-home-page', children="2 %")
                      ),
                      html.Div(
                          id="div-current-pressure-home-page",
                          children=html.Label(id='label-current-pressure-home-page', children="2 hPa")
                      ),
                      html.Div(
                          id="div-rainfall-24h-home-page",
                          children=html.Label(id='label-rainfall-24h-home-page', children="2 mm")
                      ),
                      html.Div(
                          id="div-current-wind-home-page",
                          children=html.Label(id='label-current-wind-home-page', children="2 km/h (maks. 4 km/h), E")
                      )
            ]
        )),
        dcc.Interval(
            id='interval-timer',
            interval=1 * 1000,
            n_intervals=0
        )
])


@app.callback(
    Output('label-timer-home', 'children'),
    Input('interval-timer', 'n_intervals')
)
def update_timer(n):
    return format_datetime(datetime.now(pytz.timezone('Europe/Warsaw')), format="EEE, d MMMM yyyy, HH:mm:ss", locale='pl')
