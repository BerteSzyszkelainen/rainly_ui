import pytz
from dash import dcc
from dash import html
from datetime import datetime
from dash.dependencies import Input, Output
from babel.dates import format_datetime
import dash_bootstrap_components as dbc
from dateutil.relativedelta import relativedelta
import pandas as pd

from app import app
from utilities.utilities import get_card_content, read_configuration, degrees_to_compass

CONFIG = read_configuration()
DATA_SOURCE = CONFIG['DATA']['source']

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
            ]
        ),
        html.Div(
            className="cards-container",
            children=[
                dbc.Row(
                    [
                        dbc.Col(dbc.Card(
                            color="#5585b5",
                            inverse=True,
                            id='current-rainfall-home')),
                        dbc.Col(dbc.Card(
                            color="#f95959", inverse=True,
                            id='current-temperature-home')),
                        dbc.Col(dbc.Card(
                            color="#00ccff", inverse=True,
                            id='current-humidity-home')),
                    ],
                    className="mb-4",
                ),
                dbc.Row(
                    [
                        dbc.Col(dbc.Card(
                            color="#f1b963",
                            inverse=True,
                            id='current-wind-avg-home')),
                        dbc.Col(dbc.Card(
                            color="#f1b963", inverse=True,
                            id='current-wind-max-home')),
                        dbc.Col(dbc.Card(
                            color="#f1b963",
                            inverse=True,
                            id='current-wind-direction-home')),
                    ],
                    className="mb-4",
                ),
                dbc.Row(
                    [
                        dbc.Col(dbc.Card(
                            color="#ff8c69",
                            inverse=True,
                            id='current-pressure-home')),
                    ]
                ),
            ]
        ),
        dcc.Interval(
            id='interval-timer',
            interval=1 * 1000,
            n_intervals=0
        ),
        dcc.Interval(
            id='interval-measurement',
            interval=5 * 60 * 1000,
            n_intervals=0
        )
])


@app.callback(
    Output('label-timer-home', 'children'),
    Input('interval-timer', 'n_intervals')
)
def update_timer(n):
    return format_datetime(datetime.now(pytz.timezone('Europe/Warsaw')), format="EEE, d MMMM yyyy, HH:mm:ss", locale='pl')

@app.callback(
    Output(component_id='current-temperature-home', component_property='children'),
    Output(component_id='current-humidity-home', component_property='children'),
    Output(component_id='current-pressure-home', component_property='children'),
    Output(component_id='current-rainfall-home', component_property='children'),
    Output(component_id='current-wind-avg-home', component_property='children'),
    Output(component_id='current-wind-max-home', component_property='children'),
    Output(component_id='current-wind-direction-home', component_property='children'),
    Input(component_id='interval-measurement', component_property='n_intervals')
)
def update_current_measurements(n):
    df = pd.read_json(DATA_SOURCE)
    current_temperature = df.iloc[-1]['temperature']
    current_humidity = df.iloc[-1]['humidity']
    current_pressure = df.iloc[-1]['pressure']
    current_wind_speed_avg = pd.read_json(DATA_SOURCE).iloc[-1]['wind_speed_avg']
    current_wind_speed_max = pd.read_json(DATA_SOURCE).iloc[-1]['wind_speed_max']
    current_wind_direction = degrees_to_compass(pd.read_json(DATA_SOURCE).iloc[-1]['wind_direction'])
    start_date = datetime.now() - relativedelta(days=1)
    df = df.loc[df['date'] > start_date]
    rainfall_24h = df['rainfall'].sum()
    return [
        get_card_content("Temperatura", f"{current_temperature} °C"),
        get_card_content("Wilgotność", f"{current_humidity} %"),
        get_card_content("Ciśnienie", f"{current_pressure} hPa"),
        get_card_content("Opady 24h", f"{rainfall_24h} mm"),
        get_card_content("Wiatr prędkość śr.", f"{current_wind_speed_avg} km/h"),
        get_card_content("Wiatr prędkość max.", f"{current_wind_speed_max} km/h"),
        get_card_content("Wiatr kierunek", f"{current_wind_direction}"),
    ]