from dash import html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

from app import app
from utilities.utilities import read_configuration, get_navigation, get_current_measurement_card, get_interval_timer, \
    get_interval_measurement, get_div_timer, get_current_date

CONFIG = read_configuration()
DATA_SOURCE = CONFIG['DATA']['source']
MEASUREMENT_INTERVAL = CONFIG['MEASUREMENT']['interval']


layout = html.Div(
    id="div-root-home",
    children=[
        get_div_timer(id_postfix='home'),
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
        get_interval_timer(),
        get_interval_measurement()
    ]
)


@app.callback(
    Output('div-timer-home', 'children'),
    Input('interval-timer', 'n_intervals')
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
