import pandas as pd
import plotly.express as px
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
from utilities.utilities import get_rainfall_sum_per_day, get_rainfall_sum_24h, get_card_children
from utilities.utilities import get_interval_timer
from utilities.utilities import add_common_chart_features
from utilities.utilities import get_total_rainfall_sum
from utilities.utilities import get_navigation
from utilities.utilities import read_configuration
from utilities.utilities import get_slider
from utilities.utilities import get_slider_max_and_marks
from utilities.utilities import get_slider_container_display
from utilities.utilities import get_interval_measurement
from utilities.utilities import get_warning
from utilities.utilities import get_timer
from utilities.utilities import get_current_measurement
from utilities.utilities import get_current_date
from app import app


CONFIG = read_configuration()
DATA_SOURCE = CONFIG['DATA']['source']


layout = html.Div(
    id="div-root",
    children=[
        get_timer(id_postfix='rainfall'),
        get_navigation(active='Opady'),
        get_current_measurement(id_postfix='rainfall', card_color='#557A95'),
        get_slider(id_postfix='rainfall'),
        html.Div(id="div-bar-chart-rainfall"),
        get_warning(id_postfix='rainfall'),
        get_interval_timer(),
        get_interval_measurement()
    ]
)


@app.callback(
    Output(component_id='div-bar-chart-rainfall', component_property='children'),
    Output(component_id='div-bar-chart-rainfall', component_property='style'),
    Input(component_id='slider-rainfall', component_property='value'),
    Input(component_id='interval-measurement', component_property='n_intervals')
)
def update_bar_chart(day_count, n):
    df = get_rainfall_sum_per_day(day_count=day_count)

    if df.empty:
        return {}, {'display': 'none'}
    else:
        fig = px.bar(df, x=df["day"] + '.' + df["month"], y=df["rainfall"])
        fig = add_common_chart_features(fig)
        fig.update_layout(yaxis_autorange=True)
        fig.update_layout(yaxis_title="mm")
        fig.update_traces(marker_color='#557A95')
        fig.update_traces(hovertemplate="Data: %{x}<br>Suma opadów: %{y} mm")
        return dcc.Loading(children=dcc.Graph(figure=fig)), {'display': 'block'}


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
    rainfall_sum_24h = get_rainfall_sum_24h()
    return get_card_children(
            card_header='Ostatnie 24h',
            card_paragraph=f'{rainfall_sum_24h} mm',
            card_footer=f'Czas pomiaru: ostatnie 24h'
    )


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

