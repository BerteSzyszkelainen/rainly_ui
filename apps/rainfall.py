from datetime import datetime
import pandas as pd
import plotly.express as px
import pytz
from babel.dates import format_datetime
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

from utilities.utilities import generate_slider_marks, get_rainfall_sum_per_day, apply_common_chart_features, \
    get_total_rainfall_sum, read_configuration, get_card_content, get_intervals, get_navigation, get_slider, \
    get_rainfall_sum_24h_and_start_date
import dash_bootstrap_components as dbc
from app import app

CONFIG = read_configuration()
DATA_SOURCE = CONFIG['DATA']['source']
BACKGROUND_COLOR = "#5D5C61"


layout = html.Div(
    id="div-root",
    children=[
        html.Div(
            id="div-timer-rainfall"
        ),
        get_navigation(active='Opady'),
        html.Div(
            className="cards-container",
            children=dbc.Card(color="#557A95", id='current-rainfall-24h')
        ),
        get_slider(id_postfix='rainfall'),
        html.Div(
            id="div-bar-chart-rainfall",
            children=dcc.Loading(children=dcc.Graph(id="bar-chart-rainfall"))
        ),
        html.Div(
            id="div-warning-rainfall",
            children="Oczekiwanie na pierwszy pomiar..."
        ),
        get_intervals()[0],
        get_intervals()[1]
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
    Output(component_id='current-rainfall-24h', component_property='children'),
    Input(component_id='interval-measurement', component_property='n_intervals')
)
def update_rainfall_24h(n):
    rainfall_24h, start_date = get_rainfall_sum_24h_and_start_date()
    return get_card_content("Ostatnie 24h", f"{rainfall_24h} mm", f'Czas pomiaru: od {start_date.strftime("%d.%m, %H:%M")}')


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
    Output('div-timer-rainfall', 'children'),
    Input('interval-timer', 'n_intervals')
)
def update_timer(n):
    return format_datetime(
        datetime.now(pytz.timezone('Europe/Warsaw')),
        format="EEE, d MMMM yyyy, HH:mm:ss", locale='pl'
    )

@app.callback(
    Output('slider-rainfall-output', 'children'),
    Input('slider-rainfall', 'value')
)
def update_total_rainfall_sum(day_count):
    rainfall_sum = get_total_rainfall_sum(day_count)
    if day_count == 1:
        return f"Dzisiaj: {rainfall_sum} mm"
    else:
        return f"Ostatnie {day_count} dni: {rainfall_sum} mm"

