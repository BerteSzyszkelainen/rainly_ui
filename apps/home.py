import pytz
from dash import dcc
from dash import html
from datetime import datetime
from dash.dependencies import Input, Output
from babel.dates import format_datetime
import dash_bootstrap_components as dbc

from app import app
from utilities.utilities import get_card_content

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
            className="cards-container",
            children=[
                dbc.Row(
                    [
                        dbc.Col(dbc.Card(
                            get_card_content("Opady 24h", '12 mm'),
                            color="#5585b5",
                            inverse=True,
                            id='home-current-rainfall')),
                        dbc.Col(dbc.Card(
                            get_card_content("Temperatura", '10 °C'),
                            color="#f95959", inverse=True,
                            id='home-current-temperature')),
                        dbc.Col(dbc.Card(
                            get_card_content("Wilgotność", '83 %'),
                            color="#00ccff",
                            inverse=True,
                            id='home-current-humidity')),
                    ],
                    className="mb-4",
                ),
                dbc.Row(
                    [
                        dbc.Col(dbc.Card(
                            get_card_content("Wiatr prędkość średnia", "10 km/h"),
                            color="#f1b963",
                            inverse=True,
                            id='home-current-wind')),
                        dbc.Col(dbc.Card(
                            get_card_content("Wiatr prędkość maksymalna", "21 km/h"),
                            color="#f1b963", inverse=True,
                            id='home-current-wind')),
                        dbc.Col(dbc.Card(
                            get_card_content("Wiatr kierunek", 'E'),
                            color="#f1b963",
                            inverse=True,
                            id='home-current-wind')),
                    ],
                    className="mb-4",
                ),
                dbc.Row(
                    [
                        dbc.Col(dbc.Card(
                            get_card_content("Ciśnienie", '1013 hPa'),
                            color="#ff8c69",
                            inverse=True,
                            id='home-current-pressure')),
                    ]
                ),
            ]
        ),
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
