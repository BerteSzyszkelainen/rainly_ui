import pandas as pd
import plotly.express as px
from dash import html, dcc
from dash.dependencies import Input, Output
from utilities.utilities import get_measurements, apply_common_line_chart_features, \
    apply_common_chart_features, read_configuration, get_navigation, get_slider, \
    get_current_measurement_card, get_slider_max_and_marks, get_slider_container_display, get_interval_timer, \
    get_interval_measurement, get_div_warning, get_div_timer, get_line_chart, get_div_current_measurement, \
    get_current_date
from app import app


CONFIG = read_configuration()
DATA_SOURCE = CONFIG['DATA']['source']


layout = html.Div(
    id="div-root",
    children=[
        get_div_timer(id_postfix='temperature'),
        get_navigation(active='Temperatura'),
        get_div_current_measurement(id_postfix='temperature', card_color='#f95959'),
        get_slider(id_postfix='temperature'),
        get_line_chart(id_postfix='temperature'),
        get_div_warning(id_postfix='temperature'),
        get_interval_timer(),
        get_interval_measurement()
])


@app.callback(
    Output(component_id='div-line-chart-temperature', component_property='children'),
    Output(component_id='div-line-chart-temperature', component_property='style'),
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

        return dcc.Loading(children=dcc.Graph(figure=fig)), {'display': 'block'}


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
    slider_max, slider_marks = get_slider_max_and_marks()
    slider_container_display = get_slider_container_display()
    return slider_max, slider_marks, slider_container_display


@app.callback(
    Output('div-timer-temperature', 'children'),
    Input('interval-timer', 'n_intervals')
)
def update_timer(n):
    return get_current_date()