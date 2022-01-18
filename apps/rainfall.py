from datetime import datetime
import pandas as pd
import plotly.express as px
import pytz
from babel.dates import format_datetime
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
from utilities.utilities import generate_slider_marks, get_rainfall_sum_per_day, apply_common_chart_features, \
    get_total_rainfall_sum, read_configuration
from app import app

CONFIG = read_configuration()
DATA_SOURCE = CONFIG['DATA']['source']
BACKGROUND_COLOR = "#5D5C61"


layout = html.Div(
    id="root-div",
    children=[
        html.Div(
            id="div-timer",
            children=html.Label(id='label-timer-rainfall')
        ),
        html.Div(
            id="div-navigation",
            children=[
                dcc.Link(id='home', children='Start', href='/'),
                dcc.Link(id='home', className="active", children='Opady', href='/apps/rainfall'),
                dcc.Link(id='home', children='Temperatura', href='/apps/temperature'),
                dcc.Link(id='home', children='Wilgotność', href='/apps/humidity'),
                dcc.Link(id='home', children='Ciśnienie', href='/apps/pressure'),
                dcc.Link(id='home', children='Wiatr', href='/apps/wind'),
                dcc.Link(id='home', children='Moduł analityczny', href='/apps/analysis'),
            ]
        ),
        html.Div(
            id="div-slider-rainfall",
            children=[
                html.Label(id="label-select-range-title", children='Wybierz okres czasu'),
                dcc.Slider(
                    id="slider-rainfall",
                    min=1,
                    value=7
                ),
                html.Div(id='slider-rainfall-output')
            ]
        ),
        html.Div(
            id="div-bar-chart-rainfall",
            children=dcc.Loading(children=dcc.Graph(id="bar-chart-rainfall"))
        ),
        html.Div(
            id="div-warning-rainfall",
            children=html.Label(id="label-warning-rainfall", children="Oczekiwanie na pierwszy pomiar...")
        ),
        dcc.Interval(
            id='interval-timer',
            interval=1 * 1000,
            n_intervals=0
        ),
        dcc.Interval(
            id='interval-measurement',
            interval=60 * 1000,
            n_intervals=0
        )
])


@app.callback(
    Output(component_id='bar-chart-rainfall', component_property='figure'),
    Output(component_id='bar-chart-rainfall', component_property='style'),
    Input(component_id='slider-rainfall', component_property='value'),
    Input(component_id='interval-measurement', component_property='n_intervals')
)
def update_bar_chart(day_count, n):
    df = get_rainfall_sum_per_day(day_count=day_count)

    if df.empty:
        return {}, {'display': 'none'}
    else:
        fig = px.bar(df, x=df["day"] + '.' + df["month"], y=df["rainfall"])
        fig = apply_common_chart_features(fig)
        fig.update_layout(yaxis_autorange=True)
        fig.update_layout(yaxis_title="mm")
        fig.update_traces(marker_color='#557A95')
        fig.update_traces(hovertemplate="Data: %{x}<br>Suma opadów: %{y} mm")
        return fig, {'display': 'block'}


@app.callback(
    Output(component_id='div-warning-rainfall', component_property='style'),
    Input(component_id='interval-measurement', component_property='n_intervals')
)
def update_warning(n):
    df = pd.read_json(DATA_SOURCE)

    if df.empty:
        return {'display': 'block'}


@app.callback(
    Output(component_id='slider-rainfall', component_property='max'),
    Output(component_id='slider-rainfall', component_property='marks'),
    Output(component_id='div-slider-rainfall', component_property='style'),
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
    Output('label-timer-rainfall', 'children'),
    Input('interval-timer', 'n_intervals')
)
def update_timer(n):
    return format_datetime(datetime.now(pytz.timezone('Europe/Warsaw')), format="EEEE, d MMMM yyyy, HH:mm:ss", locale='pl')

@app.callback(
    Output('slider-rainfall-output', 'children'),
    Input('slider-rainfall', 'value')
)
def update_total_rainfall_sum(day_count):
    rainfall_sum = get_total_rainfall_sum(day_count)
    return "Suma całkowita: {} mm".format(rainfall_sum)

