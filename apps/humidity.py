import pandas as pd
import plotly.express as px
from dash import html, dcc
from dash.dependencies import Input, Output
from utilities.utilities import get_measurements, get_card_children, get_last_measurement_time_and_value
from utilities.utilities import add_common_line_chart_features
from utilities.utilities import add_common_chart_features
from utilities.utilities import read_configuration
from utilities.utilities import get_navigation
from utilities.utilities import get_slider
from utilities.utilities import get_slider_max_and_marks
from utilities.utilities import get_slider_container_display
from utilities.utilities import get_interval_timer
from utilities.utilities import get_interval_measurement
from utilities.utilities import get_warning
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
        get_timer(id_postfix='humidity'),
        get_navigation(active='Wilgotność'),
        get_current_measurement(id_postfix='humidity', card_color='#00ccff'),
        get_slider(id_postfix='humidity'),
        get_line_chart(id_postfix='humidity'),
        get_warning(id_postfix='humidity'),
        get_interval_timer(),
        get_interval_measurement()
    ]
)


@app.callback(
    Output(component_id='div-line-chart-humidity', component_property='children'),
    Output(component_id='div-line-chart-humidity', component_property='style'),
    Input(component_id='slider-humidity', component_property='value'),
    Input(component_id='interval-measurement', component_property='n_intervals')
)
def update_line_chart(day_count, n):
    df = get_measurements(day_count=day_count)

    if df.empty:
        return [], {'display': 'none'}
    else:
        fig = px.line(df, x=df["date"].dt.strftime('%d.%m %H:%M'), y=df["humidity"])
        fig = add_common_chart_features(fig)
        fig = add_common_line_chart_features(fig)
        fig.update_layout(yaxis_range=[0, 100])
        fig.update_layout(yaxis_title="%")
        fig.update_traces(line_color='#00ccff')
        fig.update_traces(hovertemplate="Data: %{x}<br>Wilgotność: %{y} %")

        return dcc.Loading(children=dcc.Graph(figure=fig)), {'display': 'block'}


@app.callback(
    Output(component_id='div-warning-humidity', component_property='style'),
    Input(component_id='interval-measurement', component_property='n_intervals')
)
def update_warning(n):
    df = pd.read_json(DATA_SOURCE)

    if df.empty:
        return {'display': 'block'}


@app.callback(
    Output(component_id='current-humidity', component_property='children'),
    Input(component_id='interval-timer', component_property='n_intervals')
)
def update_current_humidity(n):
    time, humidity = get_last_measurement_time_and_value(measurement_name='humidity')
    return get_card_children(
            card_header='Aktualnie',
            card_paragraph=f'{humidity} %',
            card_footer=f'Czas pomiaru: {time}'
    )


@app.callback(
    Output(component_id='slider-humidity', component_property='max'),
    Output(component_id='slider-humidity', component_property='marks'),
    Output(component_id='div-slider-humidity', component_property='style'),
    Input(component_id='interval-measurement', component_property='n_intervals')
)
def update_slider(n):
    slider_max, slider_marks = get_slider_max_and_marks()
    slider_container_display = get_slider_container_display()
    return slider_max, slider_marks, slider_container_display


@app.callback(
    Output('div-timer-humidity', 'children'),
    Input('interval-timer', 'n_intervals')
)
def update_timer(n):
    return get_current_date()
