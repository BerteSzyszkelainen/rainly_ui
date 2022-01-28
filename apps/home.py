from dash import html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from utilities.utilities import read_configuration
from utilities.utilities import get_navigation
from utilities.utilities import get_current_measurement_card
from utilities.utilities import get_interval_timer
from utilities.utilities import get_interval_measurement
from utilities.utilities import get_timer
from utilities.utilities import get_current_date
from utilities.utilities import get_card
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
            className="cards-container",
            children=[
                dbc.Row(
                    [
                        dbc.Col(dbc.Card(get_card(id='current-rainfall-home', color='#557A95'))),
                        dbc.Col(dbc.Card(get_card(id='current-temperature-home', color='#f95959'))),
                        dbc.Col(dbc.Card(get_card(id='current-humidity-home', color='#00ccff'))),
                    ],
                    className="mb-4",
                ),
                dbc.Row(
                    [
                        dbc.Col(dbc.Card(get_card(id='current-wind-avg-home', color='#f1b963'))),
                        dbc.Col(dbc.Card(get_card(id='current-wind-max-home', color='#f1b963'))),
                        dbc.Col(dbc.Card(get_card(id='current-wind-direction-home', color='#f1b963'))),
                    ],
                    className="mb-4",
                ),
                dbc.Row(
                    [
                        dbc.Col(dbc.Card(get_card(id='current-pressure-home', color='#ff8c69'))),
                    ],
                    className="mb-4",
                ),
            ]
        ),
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
    Input(component_id='interval-measurement', component_property='n_intervals')
)
def update_current_measurements(n):
    return [
        get_current_measurement_card(card_header="Temperatura", measurement_name='temperature'),
        get_current_measurement_card(card_header="Wilgotność", measurement_name='humidity'),
        get_current_measurement_card(card_header="Ciśnienie", measurement_name='pressure'),
        get_current_measurement_card(card_header="Opady 24h", measurement_name='rainfall'),
        get_current_measurement_card(card_header="Wiatr prędkość śr.", measurement_name='wind_speed_avg'),
        get_current_measurement_card(card_header="Wiatr prędkość maks.", measurement_name='wind_speed_max'),
        get_current_measurement_card(card_header="Wiatr kierunek", measurement_name='wind_direction'),
    ]
