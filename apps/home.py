import pytz
from dash import html
from datetime import datetime
from dash.dependencies import Input, Output
from babel.dates import format_datetime
import dash_bootstrap_components as dbc
import pandas as pd

from app import app
from utilities.utilities import get_card_content, read_configuration, degrees_to_compass, get_intervals, get_navigation, \
    get_rainfall_sum_24h_and_start_date

CONFIG = read_configuration()
DATA_SOURCE = CONFIG['DATA']['source']
MEASUREMENT_INTERVAL = CONFIG['MEASUREMENT']['interval']

layout = html.Div(
    id="div-root-home",
    children=[
        html.Div(
            id="div-timer-home"
        ),
        get_navigation(active='Start'),
        html.Div(
            className="cards-container",
            children=[
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Card(
                                color="#5585b5",
                                id='current-rainfall-home'
                            )
                        ),
                        dbc.Col(
                            dbc.Card(
                                color="#f95959",
                                id='current-temperature-home'
                            )
                        ),
                        dbc.Col(
                            dbc.Card(
                                color="#00ccff",
                                id='current-humidity-home'
                            )
                        ),
                    ],
                    className="mb-4",
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Card(
                                color="#f1b963",
                                id='current-wind-avg-home'
                            )
                        ),
                        dbc.Col(
                            dbc.Card(
                                color="#f1b963",
                                id='current-wind-max-home'
                            )
                        ),
                        dbc.Col(
                            dbc.Card(
                                color="#f1b963",
                                id='current-wind-direction-home'
                            )
                        ),
                    ],
                    className="mb-4",
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Card(
                                color="#ff8c69",
                                id='current-pressure-home'
                            )
                        ),
                    ],
                    className="mb-4",
                ),
            ]
        ),
        get_intervals()[0],
        get_intervals()[1]
    ]
)


@app.callback(
    Output('div-timer-home', 'children'),
    Input('interval-timer', 'n_intervals')
)
def update_timer(n):
    return format_datetime(
        datetime.now(pytz.timezone('Europe/Warsaw')),
        format="EEE, d MMMM yyyy, HH:mm:ss", locale='pl'
    )


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
    last_measurement_time = df.iloc[-1]['date'].strftime("%d.%m, %H:%M")
    current_temperature = df.iloc[-1]['temperature']
    current_humidity = df.iloc[-1]['humidity']
    current_pressure = df.iloc[-1]['pressure']
    current_wind_speed_avg = pd.read_json(DATA_SOURCE).iloc[-1]['wind_speed_avg']
    current_wind_speed_max = pd.read_json(DATA_SOURCE).iloc[-1]['wind_speed_max']
    current_wind_direction = degrees_to_compass(pd.read_json(DATA_SOURCE).iloc[-1]['wind_direction'])
    rainfall_24h, start_date = get_rainfall_sum_24h_and_start_date()
    return [
        get_card_content(
            "Temperatura", f"{current_temperature} °C",
            f'Czas pomiaru: {last_measurement_time}'
        ),
        get_card_content(
            "Wilgotność", f"{current_humidity} %",
            f'Czas pomiaru: {last_measurement_time}'
        ),
        get_card_content(
            "Ciśnienie", f"{current_pressure} hPa",
            f'Czas pomiaru: {last_measurement_time}'
        ),
        get_card_content(
            "Opady 24h", f"{rainfall_24h} mm",
            f'Czas pomiaru: od {start_date.strftime("%d.%m, %H:%M")}'
        ),
        get_card_content(
            "Wiatr prędkość śr.",
            f"{current_wind_speed_avg} km/h",
            f'Czas pomiaru: {last_measurement_time}'
        ),
        get_card_content(
            "Wiatr prędkość max.",
            f"{current_wind_speed_max} km/h",
            f'Czas pomiaru: {last_measurement_time}'
        ),
        get_card_content(
            "Wiatr kierunek",
            f"{current_wind_direction}",
            f'Czas pomiaru: {last_measurement_time}'
        ),
    ]
