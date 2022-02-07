import pandas as pd
from dash import html, dcc
import plotly.graph_objects as go
from dash.dependencies import Input, Output
from utilities.utilities import add_common_line_chart_features, get_card
from utilities.utilities import get_last_measurement_time_and_value
from utilities.utilities import get_card_children
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
        get_timer(id_postfix='temperature'),
        get_navigation(active='Temperatura'),
        html.Div(
            id="div-current-temperature",
            children=dbc.Row(
                children=[
                    dbc.Col(dbc.Card(get_card(id='current-temperature', color='#F08080'))),
                    dbc.Col(dbc.Card(get_card(id='current-ground-temperature', color='#D14239'))),
                ],
                className="mb-5",
                style={"width": "60rem", 'margin': '0 auto', 'float': 'none'}
            )
        ),
        get_slider(id_postfix='temperature'),
        get_line_chart(id_postfix='temperature'),
        get_warning(id_postfix='temperature'),
        get_interval_timer(),
        get_interval_measurement()
    ]
)


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

        fig = go.Figure()
        date_format = '%d.%m %H:%M'

        fig.add_trace(
            go.Scatter(
                x=df["date"].dt.strftime(date_format),
                y=df["temperature"],
                name="Temperatura",
                mode='lines+markers',
                line={'color': '#F08080'},
                marker={'size': 8, 'color': ['#F08080' for item in df["temperature"]]},
            )
        )

        fig.add_trace(
            go.Scatter(
                x=df["date"].dt.strftime(date_format),
                y=df["ground_temperature"],
                name="Temperatura przy gruncie",
                mode='lines+markers',
                line={'color': '#D14239'},
                marker={'size': 8, 'color': ['#D14239' for item in df["ground_temperature"]]},
            )
        )

        fig = add_common_chart_features(fig)
        fig = add_common_line_chart_features(fig)
        fig.update_layout(yaxis_range=[-40, 50])
        fig.update_layout(yaxis_title='°C')
        fig.update_layout(showlegend=True)
        fig.update_layout(yaxis_title="°C")
        fig.update_traces(hovertemplate='Data: %{x}<br>%{y}°C')

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
    Output(component_id='current-ground-temperature', component_property='children'),
    Output(component_id='div-current-temperature', component_property='style'),
    Input(component_id='interval-measurement', component_property='n_intervals')
)
def update_current_temperature(n):
    time, temperature = get_last_measurement_time_and_value(measurement_name='temperature')
    _, ground_temperature = get_last_measurement_time_and_value(measurement_name='ground_temperature')
    style_display = get_style_display()
    return [
        get_card_children(
            card_header='Temperatura',
            card_paragraph=f'{round(temperature, 1)} °C',
            card_footer=f'Czas pomiaru: {time}'
        ),
        get_card_children(
            card_header='Temperatura przy gruncie',
            card_paragraph=f'{round(ground_temperature, 1)} °C',
            card_footer=f'Czas pomiaru: {time}'
        ),
        style_display
    ]


@app.callback(
    Output(component_id='slider-temperature', component_property='max'),
    Output(component_id='slider-temperature', component_property='marks'),
    Output(component_id='div-slider-temperature', component_property='style'),
    Input(component_id='interval-measurement', component_property='n_intervals')
)
def update_slider(n):
    slider_max, slider_marks = get_slider_max_and_marks()
    slider_container_display = get_style_display()
    return slider_max, slider_marks, slider_container_display


@app.callback(
    Output('div-timer-temperature', 'children'),
    Input('interval-timer', 'n_intervals')
)
def update_timer(n):
    return get_current_date()