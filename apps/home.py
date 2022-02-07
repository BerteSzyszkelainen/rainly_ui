from dash import html
from dash.dependencies import Input
from dash.dependencies import Output
import dash_bootstrap_components as dbc
from utilities.utilities import read_configuration
from utilities.utilities import get_card_children
from utilities.utilities import get_last_measurement_time_and_value
from utilities.utilities import get_rainfall_sum_24h
from utilities.utilities import get_style_display
from utilities.utilities import get_warning
from utilities.utilities import get_navigation
from utilities.utilities import get_interval_timer
from utilities.utilities import get_interval_measurement
from utilities.utilities import get_timer
from utilities.utilities import get_current_date
from utilities.utilities import get_card
import pandas as pd
from app import app


CONFIG = read_configuration()
DATA_SOURCE = CONFIG['DATA']['source']
MEASUREMENT_INTERVAL = CONFIG['MEASUREMENT']['interval']


layout = html.Div(
    id="div-root-home",
    children=[
        get_timer(id_postfix='home'),
        get_navigation(active='Start'),
        html.Div(
            id="div-current-measurements",
            children=[
                dbc.Row(
                    [
                        dbc.Col(dbc.Card(get_card(id='current-rainfall-home', color='#557A95'))),
                        dbc.Col(dbc.Card(get_card(id='current-temperature-home', color='#F08080'))),
                        dbc.Col(dbc.Card(get_card(id='current-ground-temperature-home', color='#D14239'))),
                    ],
                    className="mb-1",
                    style={"width": "60rem", 'margin': '0 auto', 'float': 'none'}
                ),
                dbc.Row(
                    [
                        dbc.Col(dbc.Card(get_card(id='current-wind-avg-home', color='#E2B864'))),
                        dbc.Col(dbc.Card(get_card(id='current-wind-max-home', color='#E2B864'))),
                        dbc.Col(dbc.Card(get_card(id='current-wind-direction-home', color='#EAA42E'))),
                    ],
                    className="mb-1",
                    style={"width": "60rem", 'margin': '0 auto', 'float': 'none'}
                ),
                dbc.Row(
                    [
                        dbc.Col(dbc.Card(get_card(id='current-humidity-home', color='#00ccff'))),
                        dbc.Col(dbc.Card(get_card(id='current-air-quality-pm-two-five-home', color='#D39CB6'))),
                        dbc.Col(dbc.Card(get_card(id='current-air-quality-pm-ten-home', color='#755F91'))),
                    ],
                    className="mb-1",
                    style={"width": "60rem", 'margin': '0 auto', 'float': 'none'}
                ),
                dbc.Row(
                    [
                        dbc.Col(dbc.Card(get_card(id='current-pressure-home', color='#ff8c69'))),
                    ],
                    className="mb-1",
                    style={"width": "20rem", 'margin': '0 auto', 'float': 'none'}
                )
            ],
        ),
        get_warning(id_postfix='home'),
        get_interval_timer(),
        get_interval_measurement()
    ]
)


@app.callback(
    Output(component_id='div-timer-home', component_property='children'),
    Input(component_id='interval-timer', component_property='n_intervals')
)
def update_timer(n):
    return get_current_date()


@app.callback(
    Output(component_id='current-temperature-home', component_property='children'),
    Output(component_id='current-ground-temperature-home', component_property='children'),
    Output(component_id='current-humidity-home', component_property='children'),
    Output(component_id='current-pressure-home', component_property='children'),
    Output(component_id='current-rainfall-home', component_property='children'),
    Output(component_id='current-wind-avg-home', component_property='children'),
    Output(component_id='current-wind-max-home', component_property='children'),
    Output(component_id='current-wind-direction-home', component_property='children'),
    Output(component_id='current-air-quality-pm-two-five-home', component_property='children'),
    Output(component_id='current-air-quality-pm-ten-home', component_property='children'),
    Output(component_id='div-current-measurements', component_property='style'),
    Input(component_id='interval-measurement', component_property='n_intervals')
)
def update_current_measurements(n):
    time, temperature = get_last_measurement_time_and_value(measurement_name='temperature')
    _, ground_temperature = get_last_measurement_time_and_value(measurement_name='ground_temperature')
    _, humidity = get_last_measurement_time_and_value(measurement_name='humidity')
    _, pressure = get_last_measurement_time_and_value(measurement_name='pressure')
    _, wind_speed_avg = get_last_measurement_time_and_value(measurement_name='wind_speed_avg')
    _, wind_speed_max = get_last_measurement_time_and_value(measurement_name='wind_speed_max')
    _, wind_direction = get_last_measurement_time_and_value(measurement_name='wind_direction')
    _, pm_two_five = get_last_measurement_time_and_value(measurement_name='pm_two_five')
    _, pm_ten = get_last_measurement_time_and_value(measurement_name='pm_ten')
    rainfall_sum_24h = get_rainfall_sum_24h()
    style_display = get_style_display()

    return [
        get_card_children(
            card_header='Temperatura',
            card_paragraph=f'{round(temperature, 1)} °C',
            card_footer=f'Czas pomiaru: {time}'
        ),
        get_card_children(
            card_header='Temperatura przy gruncie',
            card_paragraph=f'{round(ground_temperature, 1)} °C',
            card_footer=f'Czas pomiaru: {time}'
        ),
        get_card_children(
            card_header='Wilgotność',
            card_paragraph=f'{round(humidity, 1)} %',
            card_footer=f'Czas pomiaru: {time}'
        ),
        get_card_children(
            card_header='Ciśnienie',
            card_paragraph=f'{round(pressure, 1)} hPa',
            card_footer=f'Czas pomiaru: {time}'
        ),
        get_card_children(
            card_header='Opady 24h',
            card_paragraph=f'{round(rainfall_sum_24h, 1)} mm',
            card_footer=f'Czas pomiaru: ostatnie 24h'
        ),
        get_card_children(
            card_header='Wiatr prędkość śr.',
            card_paragraph=f'{round(wind_speed_avg, 1)} km/h',
            card_footer=f'Czas pomiaru: {time}'
        ),
        get_card_children(
            card_header='Wiatr prędkość maks.',
            card_paragraph=f'{round(wind_speed_max, 1)} km/h',
            card_footer=f'Czas pomiaru: {time}'
        ),
        get_card_children(
            card_header='Wiatr kierunek',
            card_paragraph=f'{wind_direction}',
            card_footer=f'Czas pomiaru: {time}'
        ),
        get_card_children(
            card_header='Cząsteczki PM2.5',
            card_paragraph=f'{round(pm_two_five, 1)} mikrograma/m3',
            card_footer=f'Czas pomiaru: {time}'
        ),
        get_card_children(
            card_header='Cząsteczki PM10',
            card_paragraph=f'{round(pm_ten, 1)} mikrograma/m3',
            card_footer=f'Czas pomiaru: {time}'
        ),
        style_display
    ]


@app.callback(
    Output(component_id='div-warning-home', component_property='style'),
    Input(component_id='interval-measurement', component_property='n_intervals')
)
def update_warning(n):
    df = pd.read_json(DATA_SOURCE)

    if df.empty:
        return {'display': 'block'}