import pandas as pd
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from utilities.utilities import degrees_to_compass, get_card, get_card_children, get_last_measurement_time_and_value
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
from utilities.utilities import get_current_date
import dash_bootstrap_components as dbc
from app import app


CONFIG = read_configuration()
DATA_SOURCE = CONFIG['DATA']['source']


layout = html.Div(
    id="div-root",
    children=[
        get_timer(id_postfix='wind'),
        get_navigation(active='Wiatr'),
        html.Div(
            id="div-current-wind",
            children=dbc.Row(
                children=[
                    dbc.Col(dbc.Card(get_card(id='current-wind-avg', color='#f1b963'))),
                    dbc.Col(dbc.Card(get_card(id='current-wind-max', color='#f1b963'))),
                    dbc.Col(dbc.Card(get_card(id='current-wind-direction', color='#f1b963'))),
                ]
            )
        ),
        get_slider(id_postfix='wind'),
        get_line_chart(id_postfix='wind'),
        get_warning(id_postfix='wind'),
        get_interval_timer(),
        get_interval_measurement()
    ]
)


@app.callback(
    Output(component_id='div-line-chart-wind', component_property='children'),
    Output(component_id='div-line-chart-wind', component_property='style'),
    Input(component_id='slider-wind', component_property='value'),
    Input(component_id='interval-measurement', component_property='n_intervals')
)
def update_line_chart(day_count, n):
    df = get_measurements(day_count=day_count)

    if df.empty:
        return {}, {'display': 'none'}
    else:
        fig = go.Figure()
        date_format = '%d.%m %H:%M'

        fig.add_trace(
            go.Scatter(
                x=df["date"].dt.strftime(date_format),
                y=df["wind_speed_avg"],
                name="prędkość śr.",
                mode='lines+markers',
                marker={'size': 8}
            )
        )

        fig.add_trace(
            go.Scatter(
                x=df["date"].dt.strftime(date_format),
                y=df["wind_speed_max"],
                name="prędkość maks.",
                mode='lines+markers',
                marker={'size': 8}
            )
        )

        fig.add_trace(
            go.Scatter(
                x=df["date"].dt.strftime(date_format),
                y=df["wind_speed_max"] + 20,
                name="kierunek",
                mode="markers+text",
                text=df["wind_direction"].apply(lambda x: degrees_to_compass(x)),
                textposition="top center",
                textfont={
                    'size': 12,
                    'color': 'white'
                },
                marker={'size': 8}
            )
        )

        fig = add_common_chart_features(fig)
        fig.update_layout(showlegend=True)
        fig.update_layout(yaxis_range=[0, 150])
        fig.update_layout(yaxis_title="km/h")
        fig.update_traces(hovertemplate="Data: %{x}<br>Prędkość: %{y} km/h <extra></extra>")

        return dcc.Loading(children=dcc.Graph(figure=fig)), {'display': 'block'}


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
    Output(component_id='div-current-wind', component_property='style'),
    Input(component_id='interval-measurement', component_property='n_intervals')
)
def update_current_wind(n):
    time, wind_speed_avg = get_last_measurement_time_and_value(measurement_name='wind_speed_avg')
    _, wind_speed_max = get_last_measurement_time_and_value(measurement_name='wind_speed_max')
    _, wind_direction = get_last_measurement_time_and_value(measurement_name='wind_direction')
    wind_direction = degrees_to_compass(wind_direction)
    style_display = get_style_display()
    return [
        get_card_children(
            card_header='Prędkość śr.',
            card_paragraph=f'{wind_speed_avg} km/h',
            card_footer=f'Czas pomiaru: {time}'
        ),
        get_card_children(
            card_header='Prędkość maks.',
            card_paragraph=f'{wind_speed_max} km/h',
            card_footer=f'Czas pomiaru: {time}'
        ),
        get_card_children(
            card_header='Kierunek',
            card_paragraph=f'{wind_direction}',
            card_footer=f'Czas pomiaru: {time}'
        ),
        style_display
    ]


@app.callback(
    Output(component_id='slider-wind', component_property='max'),
    Output(component_id='slider-wind', component_property='marks'),
    Output(component_id='div-slider-wind', component_property='style'),
    Input(component_id='interval-measurement', component_property='n_intervals')
)
def update_slider(n):
    slider_max, slider_marks = get_slider_max_and_marks()
    slider_container_display = get_style_display()
    return slider_max, slider_marks, slider_container_display


@app.callback(
    Output('div-timer-wind', 'children'),
    Input('interval-timer', 'n_intervals')
)
def update_timer(n):
    return get_current_date()
