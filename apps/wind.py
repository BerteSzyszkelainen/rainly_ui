from datetime import datetime
import pandas as pd
import pytz
from babel.dates import format_datetime
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from utilities.utilities import generate_slider_marks, degrees_to_compass, \
    get_measurements, apply_common_chart_features, read_configuration, get_card_content
import dash_bootstrap_components as dbc
from app import app

CONFIG = read_configuration()
DATA_SOURCE = CONFIG['DATA']['source']
BACKGROUND_COLOR = "#5D5C61"


layout = html.Div(
    id="root-div",
    children=[
        html.Div(
            id="div-timer",
            children=html.Label(id='label-timer-wind')
        ),
        html.Div(
            id="div-navigation",
            children=[
                dcc.Link(id='home', children='Start', href='/'),
                dcc.Link(id='home', children='Opady', href='/apps/rainfall'),
                dcc.Link(id='home', children='Temperatura', href='/apps/temperature'),
                dcc.Link(id='home', children='Wilgotność', href='/apps/humidity'),
                dcc.Link(id='home', children='Ciśnienie', href='/apps/pressure'),
                dcc.Link(id='home', className="active", children='Wiatr', href='/apps/wind')
            ]
        ),
        html.Div(
            className="cards-container",
            children=dbc.Row(
                children=[
                    dbc.Col(dbc.Card(
                        color="#f1b963",
                        inverse=True,
                        id='current-wind-avg')),
                    dbc.Col(dbc.Card(
                        color="#f1b963", inverse=True,
                        id='current-wind-max')),
                    dbc.Col(dbc.Card(
                        color="#f1b963",
                        inverse=True,
                        id='current-wind-direction')),
                ],
                className="mb-4",
            )
        ),
        html.Div(
            id="div-slider-wind",
            children=[
                html.Label(id="label-select-range-title", children='Wybierz okres czasu'),
                dcc.Slider(
                    id="slider-wind",
                    min=1,
                    value=7,
                )
            ]
        ),
        html.Div(
            id="div-line-chart-wind",
            children=dcc.Loading(children=dcc.Graph(id="line-chart-wind"))
        ),
        html.Div(
            id="div-warning-wind",
            children=html.Label(id="label-warning", children="Oczekiwanie na pierwszy pomiar...")
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
    Output(component_id='line-chart-wind', component_property='figure'),
    Output(component_id='line-chart-wind', component_property='style'),
    Input(component_id='slider-wind', component_property='value'),
    Input(component_id='interval-measurement', component_property='n_intervals')
)
def update_line_chart(day_count, n):

    df = get_measurements(day_count=day_count)

    if df.empty:
        return {}, {'display': 'none'}
    else:
        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=df["date"].dt.strftime('%d.%m %H:%M'),
                y=df["wind_speed_avg"],
                name="prędkość śr.",
                mode='lines+markers',
                marker={'size': 8}
            )
        )

        fig.add_trace(
            go.Scatter(
                x=df["date"].dt.strftime('%d.%m %H:%M'),
                y=df["wind_speed_max"],
                name="prędkość maks.",
                mode='lines+markers',
                marker={'size': 8}
            )
        )

        fig.add_trace(
            go.Scatter(
                x=df["date"].dt.strftime('%d.%m %H:%M'),
                y=df["wind_speed_max"]+20,
                name="kierunek",
                mode="markers+text",
                text=df["wind_speed_max"].apply(lambda x: degrees_to_compass(x)),
                textposition="top center",
                textfont={
                    'size': 12,
                    'color': 'white'
                },
                marker={'size': 12}
            )
        )

        fig = apply_common_chart_features(fig)
        fig.update_layout(showlegend=True)
        fig.update_layout(yaxis_range=[0, 150])
        fig.update_layout(yaxis_title="km/h")
        fig.update_traces(hovertemplate="Data: %{x}<br>Prędkość: %{y} km/h <extra></extra>")

        return fig, {'display': 'block'}


@app.callback(
    Output(component_id='div-warning-wind', component_property='style'),
    Input(component_id='interval-measurement', component_property='n_intervals')
)
def update_warning(n):

    df = pd.read_json(DATA_SOURCE)

    if df.empty:
        return {'display': 'block'}

@app.callback(
    Output(component_id='current-wind-avg', component_property='children'),
    Output(component_id='current-wind-max', component_property='children'),
    Output(component_id='current-wind-direction', component_property='children'),
    Input(component_id='interval-measurement', component_property='n_intervals')
)
def update_current_wind(n):
    last_measurement_time = pd.read_json(DATA_SOURCE).iloc[-1]['date'].strftime("%d.%m, %H:%M")
    current_wind_speed_avg = pd.read_json(DATA_SOURCE).iloc[-1]['wind_speed_avg']
    current_wind_speed_max = pd.read_json(DATA_SOURCE).iloc[-1]['wind_speed_max']
    current_wind_direction = degrees_to_compass(pd.read_json(DATA_SOURCE).iloc[-1]['wind_direction'])
    return [
        get_card_content("Prędkość śr.", f"{current_wind_speed_avg} km/h", f'Czas pomiaru: {last_measurement_time}'),
        get_card_content("Prędkość maks.", f"{current_wind_speed_max} km/h", f'Czas pomiaru: {last_measurement_time}'),
        get_card_content("Kierunek", f"{current_wind_direction}", f'Czas pomiaru: {last_measurement_time}')
    ]


@app.callback(
    Output(component_id='slider-wind', component_property='max'),
    Output(component_id='slider-wind', component_property='marks'),
    Output(component_id='div-slider-wind', component_property='style'),
    Input(component_id='interval-measurement', component_property='n_intervals')
)
def update_slider(n):

    df = pd.read_json(DATA_SOURCE)

    if df.empty:
        return None, {}, {'display': 'none'}
    else:
        day_count = df.groupby([df["date"].dt.year, df["date"].dt.month, df["date"].dt.day], as_index=False).ngroups
        if day_count > 28:
            day_count = 28
        return day_count, generate_slider_marks(day_count, tick_postfix='d'), {'display': 'block'}


@app.callback(
    Output('label-timer-wind', 'children'),
    Input('interval-timer', 'n_intervals')
)
def update_timer(n):
    return format_datetime(datetime.now(pytz.timezone('Europe/Warsaw')), format="EEEE, d MMMM yyyy, HH:mm:ss", locale='pl')