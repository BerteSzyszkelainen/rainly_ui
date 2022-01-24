from datetime import datetime
import pandas as pd
import plotly.express as px
import pytz
from babel.dates import format_datetime
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
from utilities.utilities import generate_slider_marks, apply_common_line_chart_features, get_measurements, \
    apply_common_chart_features, read_configuration, get_card_content
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
            children=html.Label(id='label-timer-humidity')
        ),
        html.Div(
            id="div-navigation",
            children=[
                dcc.Link(id='home', children='Start', href='/'),
                dcc.Link(id='home', children='Opady', href='/apps/rainfall'),
                dcc.Link(id='home', children='Temperatura', href='/apps/temperature'),
                dcc.Link(id='home', className="active", children='Wilgotność', href='/apps/humidity'),
                dcc.Link(id='home', children='Ciśnienie', href='/apps/pressure'),
                dcc.Link(id='home', children='Wiatr', href='/apps/wind')
            ]
        ),
        html.Div(
            className="cards-container",
            children=dbc.Card(color="#00ccff", id='current-humidityy')
        ),
        html.Div(
            id="div-slider-humidity",
            children=[
                html.Label(id="label-select-range-title", children='Wybierz okres czasu'),
                dcc.Slider(
                    id="slider-humidity",
                    min=1,
                    value=7,
                )
            ]
        ),
        html.Div(
            id="div-line-chart-humidity",
            children=dcc.Loading(children=dcc.Graph(id="line-chart-humidity"))
        ),
        html.Div(
            id="div-warning-humidity",
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
    Output(component_id='line-chart-humidity', component_property='figure'),
    Output(component_id='line-chart-humidity', component_property='style'),
    Input(component_id='slider-humidity', component_property='value'),
    Input(component_id='interval-measurement', component_property='n_intervals')
)
def update_line_chart(day_count, n):

    df = get_measurements(day_count=day_count)

    if df.empty:
        return {}, {'display': 'none'}
    else:
        fig = px.line(df, x=df["date"].dt.strftime('%d.%m %H:%M'), y=df["humidity"])
        fig = apply_common_chart_features(fig)
        fig = apply_common_line_chart_features(fig)
        fig.update_layout(yaxis_range=[0, 100])
        fig.update_layout(yaxis_title="%")
        fig.update_traces(line_color='#00ccff')
        fig.update_traces(hovertemplate="Data: %{x}<br>Wilgotność: %{y} %")

        return fig, {'display': 'block'}


@app.callback(
    Output(component_id='div-warning-humidity', component_property='style'),
    Input(component_id='interval-measurement', component_property='n_intervals')
)
def update_warning(n):

    df = pd.read_json(DATA_SOURCE)

    if df.empty:
        return {'display': 'block'}

@app.callback(
    Output(component_id='current-humidityy', component_property='children'),
    Input(component_id='interval-timer', component_property='n_intervals')
)
def update_current_humidity(n):
    current_humidity = pd.read_json(DATA_SOURCE).iloc[-1]['humidity']
    last_measurement_time = pd.read_json(DATA_SOURCE).iloc[-1]['date'].strftime("%d.%m, %H:%M")
    return get_card_content("Aktualnie", f"{current_humidity} %", f'Czas pomiaru: {last_measurement_time}')


@app.callback(
    Output(component_id='slider-humidity', component_property='max'),
    Output(component_id='slider-humidity', component_property='marks'),
    Output(component_id='div-slider-humidity', component_property='style'),
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
    Output('label-timer-humidity', 'children'),
    Input('interval-timer', 'n_intervals')
)
def update_timer(n):
    return format_datetime(datetime.now(pytz.timezone('Europe/Warsaw')), format="EEEE, d MMMM yyyy, HH:mm:ss", locale='pl')
