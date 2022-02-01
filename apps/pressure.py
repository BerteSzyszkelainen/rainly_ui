import pandas as pd
import plotly.express as px
from dash import html, dcc
from dash.dependencies import Input, Output
from utilities.utilities import add_common_line_chart_features, get_card_children, get_last_measurement_time_and_value
from utilities.utilities import get_measurements
from utilities.utilities import add_common_chart_features
from utilities.utilities import read_configuration
from utilities.utilities import get_navigation
from utilities.utilities import get_slider
from utilities.utilities import get_slider_max_and_marks
from utilities.utilities import get_style_display
from utilities.utilities import get_interval_timer
from utilities.utilities import get_warning
from utilities.utilities import get_interval_measurement
from utilities.utilities import get_timer
from utilities.utilities import get_line_chart
from utilities.utilities import get_current_measurement
from utilities.utilities import get_current_date
from app import app


CONFIG = read_configuration()
DATA_SOURCE = CONFIG['DATA']['source']


layout = html.Div(
    id="div-root",
    children=[
        get_timer(id_postfix='pressure'),
        get_navigation(active='Ciśnienie'),
        get_current_measurement(id_postfix='pressure', card_color='#ff8c69'),
        get_slider(id_postfix='pressure'),
        get_line_chart(id_postfix='pressure'),
        get_warning(id_postfix='pressure'),
        get_interval_timer(),
        get_interval_measurement()
    ]
)


@app.callback(
    Output(component_id='div-line-chart-pressure', component_property='children'),
    Output(component_id='div-line-chart-pressure', component_property='style'),
    Input(component_id='slider-pressure', component_property='value'),
    Input(component_id='interval-measurement', component_property='n_intervals')
)
def update_line_chart(day_count, n):
    df = get_measurements(day_count=day_count)

    if df.empty:
        return {}, {'display': 'none'}
    else:
        fig = px.line(df, x=df["date"].dt.strftime('%d.%m %H:%M'), y=df["pressure"])
        fig = add_common_chart_features(fig)
        fig = add_common_line_chart_features(fig)
        fig.update_layout(yaxis_range=[900, 1200])
        fig.update_layout(yaxis_title="hPa")
        fig.update_traces(line_color='#ff8c69')
        fig.update_traces(hovertemplate="Data: %{x}<br>Ciśnienie atmosferyczne: %{y} hPa")

        return dcc.Loading(children=dcc.Graph(figure=fig)), {'display': 'block'}


@app.callback(
    Output(component_id='div-warning-pressure', component_property='style'),
    Input(component_id='interval-measurement', component_property='n_intervals')
)
def update_warning(n):
    df = pd.read_json(DATA_SOURCE)

    if df.empty:
        return {'display': 'block'}


@app.callback(
    Output(component_id='current-pressure', component_property='children'),
    Output(component_id='div-current-pressure', component_property='style'),
    Input(component_id='interval-measurement', component_property='n_intervals')
)
def update_current_pressure(n):
    time, pressure = get_last_measurement_time_and_value(measurement_name='pressure')
    style_display = get_style_display()
    return get_card_children(
        card_header='Aktualnie',
        card_paragraph=f'{pressure} hPa',
        card_footer=f'Czas pomiaru: {time}'
    ), style_display


@app.callback(
    Output(component_id='slider-pressure', component_property='max'),
    Output(component_id='slider-pressure', component_property='marks'),
    Output(component_id='div-slider-pressure', component_property='style'),
    Input(component_id='interval-measurement', component_property='n_intervals')
)
def update_slider(n):
    slider_max, slider_marks = get_slider_max_and_marks()
    slider_container_display = get_style_display()
    return slider_max, slider_marks, slider_container_display


@app.callback(
    Output('div-timer-pressure', 'children'),
    Input('interval-timer', 'n_intervals')
)
def update_timer(n):
    return get_current_date()