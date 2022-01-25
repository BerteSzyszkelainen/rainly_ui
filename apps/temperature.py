from datetime import datetime
import pandas as pd
import plotly.express as px
import pytz
from babel.dates import format_datetime
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
from utilities.utilities import generate_slider_marks, get_measurements, apply_common_line_chart_features, \
    apply_common_chart_features, read_configuration, get_card_content, get_intervals, get_navigation, get_slider, \
    get_current_measurement_card
import dash_bootstrap_components as dbc
from app import app


CONFIG = read_configuration()
DATA_SOURCE = CONFIG['DATA']['source']


layout = html.Div(
    id="div-root",
    children=[
        html.Div(
            id="div-timer-temperature"
        ),
        get_navigation(active='Temperatura'),
        html.Div(
            className="cards-container",
            children=dbc.Card(color="#f95959", id='current-temperature')
        ),
        get_slider(id_postfix='temperature'),
        html.Div(
            id="div-line-chart-temperature",
            children=dcc.Loading(children=dcc.Graph(id="line-chart-temperature"))
        ),
        html.Div(
            id="div-warning-temperature",
            children="Oczekiwanie na pierwszy pomiar..."
        ),
        get_intervals()[0],
        get_intervals()[1]
])


@app.callback(
    Output(component_id='line-chart-temperature', component_property='figure'),
    Output(component_id='line-chart-temperature', component_property='style'),
    Input(component_id='slider-temperature', component_property='value'),
    Input(component_id='interval-measurement', component_property='n_intervals')
)
def update_line_chart(day_count, n):
    df = get_measurements(day_count=day_count)

    if df.empty:
        return {}, {'display': 'none'}
    else:
        fig = px.line(df, x=df["date"].dt.strftime('%d.%m %H:%M'), y=df["temperature"])
        fig = apply_common_chart_features(fig)
        fig = apply_common_line_chart_features(fig)
        fig.update_layout(yaxis_range=[-40, 50])
        fig.update_layout(yaxis_title='°C')
        fig.update_traces(line_color='#f95959')
        fig.update_traces(hovertemplate='Data: %{x}<br>Temperatura: %{y}°C')

        return fig, {'display': 'block'}


@app.callback(
    Output(component_id='div-warning-temperature', component_property='style'),
    Input(component_id='interval-measurement', component_property='n_intervals')
)
def update_warning(n):
    df = pd.read_json(DATA_SOURCE)

    if df.empty:
        return {'display': 'block'}

@app.callback(
    Output(component_id='current-temperature', component_property='children'),
    Input(component_id='interval-measurement', component_property='n_intervals')
)
def update_current_temperature(n):
    return get_current_measurement_card('temperature')


@app.callback(
    Output(component_id='slider-temperature', component_property='max'),
    Output(component_id='slider-temperature', component_property='marks'),
    Output(component_id='div-slider-temperature', component_property='style'),
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
    Output('div-timer-temperature', 'children'),
    Input('interval-timer', 'n_intervals')
)
def update_timer(n):
    return format_datetime(
        datetime.now(pytz.timezone('Europe/Warsaw')),
        format="EEE, d MMMM yyyy, HH:mm:ss", locale='pl'
    )