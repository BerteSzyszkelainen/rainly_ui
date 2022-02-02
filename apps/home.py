from dash import html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from utilities.utilities import read_configuration, get_card_children, get_last_measurement_time_and_value, \
    get_rainfall_sum_24h, degrees_to_compass, get_style_display, get_warning
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
                        dbc.Col(dbc.Card(get_card(id='current-temperature-home', color='#f95959'))),
                        dbc.Col(dbc.Card(get_card(id='current-humidity-home', color='#00ccff'))),
                    ],
                    className="mb-3",
                    style={"width": "60rem", 'margin': '0 auto', 'float': 'none'}
                ),
                dbc.Row(
                    [
                        dbc.Col(dbc.Card(get_card(id='current-wind-avg-home', color='#f1b963'))),
                        dbc.Col(dbc.Card(get_card(id='current-wind-max-home', color='#f1b963'))),
                        dbc.Col(dbc.Card(get_card(id='current-wind-direction-home', color='#f1b963'))),
                    ],
                    className="mb-3",
                    style={"width": "60rem", 'margin': '0 auto', 'float': 'none'}
                ),
                dbc.Row(
                    [
                        dbc.Col(dbc.Card(get_card(id='current-pressure-home', color='#ff8c69'))),
                    ],
                    style={"width": "20rem", 'margin': '0 auto', 'float': 'none'}
                ),
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
    Output(component_id='current-humidity-home', component_property='children'),
    Output(component_id='current-pressure-home', component_property='children'),
    Output(component_id='current-rainfall-home', component_property='children'),
    Output(component_id='current-wind-avg-home', component_property='children'),
    Output(component_id='current-wind-max-home', component_property='children'),
    Output(component_id='current-wind-direction-home', component_property='children'),
    Output(component_id='div-current-measurements', component_property='style'),
    Input(component_id='interval-measurement', component_property='n_intervals')
)
def update_current_measurements(n):
    time, temperature = get_last_measurement_time_and_value(measurement_name='temperature')
    _, humidity = get_last_measurement_time_and_value(measurement_name='humidity')
    _, pressure = get_last_measurement_time_and_value(measurement_name='pressure')
    _, wind_speed_avg = get_last_measurement_time_and_value(measurement_name='wind_speed_avg')
    _, wind_speed_max = get_last_measurement_time_and_value(measurement_name='wind_speed_max')
    _, wind_direction = get_last_measurement_time_and_value(measurement_name='wind_direction')
    wind_direction = degrees_to_compass(wind_direction)
    rainfall_sum_24h = get_rainfall_sum_24h()
    style_display = get_style_display()

    return [
        get_card_children(
            card_header='Temperatura',
            card_paragraph=f'{round(temperature, 1)} °C',
            card_footer=f'Czas pomiaru: {time}'
        ),
        get_card_children(
            card_header='Wilgotność',
            card_paragraph=f'{humidity} %',
            card_footer=f'Czas pomiaru: {time}'
        ),
        get_card_children(
            card_header='Ciśnienie',
            card_paragraph=f'{pressure} hPa',
            card_footer=f'Czas pomiaru: {time}'
        ),
        get_card_children(
            card_header='Opady 24h',
            card_paragraph=f'{rainfall_sum_24h} mm',
            card_footer=f'Czas pomiaru: ostatnie 24h'
        ),
        get_card_children(
            card_header='Wiatr prędkość śr.',
            card_paragraph=f'{wind_speed_avg} km/h',
            card_footer=f'Czas pomiaru: {time}'
        ),
        get_card_children(
            card_header='Wiatr prędkość maks.',
            card_paragraph=f'{wind_speed_max} km/h',
            card_footer=f'Czas pomiaru: {time}'
        ),
        get_card_children(
            card_header='Wiatr kierunek',
            card_paragraph=f'{wind_direction}',
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