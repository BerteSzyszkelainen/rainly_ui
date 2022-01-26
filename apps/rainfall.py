import pandas as pd
import plotly.express as px
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

from utilities.utilities import get_rainfall_sum_per_day, apply_common_chart_features, \
    get_total_rainfall_sum, read_configuration, get_navigation, get_slider, \
    get_slider_max_and_marks, get_slider_container_display, get_current_measurement_card, get_interval_timer, \
    get_interval_measurement, get_div_warning, get_div_timer, get_div_current_measurement, get_current_date
from app import app

CONFIG = read_configuration()
DATA_SOURCE = CONFIG['DATA']['source']
BACKGROUND_COLOR = "#5D5C61"


layout = html.Div(
    id="div-root",
    children=[
        get_div_timer(id_postfix='rainfall'),
        get_navigation(active='Opady'),
        get_div_current_measurement(id_postfix='rainfall', card_color='#557A95'),
        get_slider(id_postfix='rainfall'),
        html.Div(
            id="div-bar-chart-rainfall",
            children=dcc.Loading(children=dcc.Graph(id="bar-chart-rainfall"))
        ),
        get_div_warning(id_postfix='rainfall'),
        get_interval_timer(),
        get_interval_measurement()
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
    Output(component_id='current-rainfall', component_property='children'),
    Input(component_id='interval-measurement', component_property='n_intervals')
)
def update_rainfall_24h(n):
    return get_current_measurement_card(card_header="Ostatnie 24h", measurement_name='rainfall')


@app.callback(
    Output(component_id='slider-rainfall', component_property='max'),
    Output(component_id='slider-rainfall', component_property='marks'),
    Output(component_id='div-slider-rainfall', component_property='style'),
    Input(component_id='interval-measurement', component_property='n_intervals')
)
def update_slider(n):
    slider_max, slider_marks = get_slider_max_and_marks()
    slider_container_display = get_slider_container_display()
    return slider_max, slider_marks, slider_container_display


@app.callback(
    Output('div-timer-rainfall', 'children'),
    Input('interval-timer', 'n_intervals')
)
def update_timer(n):
    return get_current_date()

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

