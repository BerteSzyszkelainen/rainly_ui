import pandas as pd
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from utilities.utilities import degrees_to_compass, \
    get_measurements, apply_common_chart_features, read_configuration, get_navigation, \
    get_slider, get_slider_max_and_marks, get_slider_container_display, get_current_measurement_card, \
    get_interval_timer, get_interval_measurement, get_div_warning, get_div_timer, get_line_chart, get_current_date
import dash_bootstrap_components as dbc
from app import app

CONFIG = read_configuration()
DATA_SOURCE = CONFIG['DATA']['source']
BACKGROUND_COLOR = "#5D5C61"

layout = html.Div(
    id="div-root",
    children=[
        get_div_timer(id_postfix='wind'),
        get_navigation(active='Wiatr'),
        html.Div(
            className="cards-container",
            children=dbc.Row(
                children=[
                    dbc.Col(dbc.Card(
                        color="#f1b963",
                        id='current-wind-avg')),
                    dbc.Col(dbc.Card(
                        color="#f1b963",
                        id='current-wind-max')),
                    dbc.Col(dbc.Card(
                        color="#f1b963",
                        id='current-wind-direction')),
                ],
                className="mb-4",
            )
        ),
        get_slider(id_postfix='wind'),
        get_line_chart(id_postfix='wind'),
        get_div_warning(id_postfix='wind'),
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

        fig.add_trace(
            go.Scatter(
                x=df["date"].dt.strftime('%d.%m %H:%M'),
                y=df["wind_speed_avg"],
                name="prędkość śr.",
                mode='lines+markers',
                marker={'size': 8}
            )
        )

        fig.add_trace(
            go.Scatter(
                x=df["date"].dt.strftime('%d.%m %H:%M'),
                y=df["wind_speed_max"],
                name="prędkość maks.",
                mode='lines+markers',
                marker={'size': 8}
            )
        )

        fig.add_trace(
            go.Scatter(
                x=df["date"].dt.strftime('%d.%m %H:%M'),
                y=df["wind_speed_max"] + 20,
                name="kierunek",
                mode="markers+text",
                text=df["wind_speed_max"].apply(lambda x: degrees_to_compass(x)),
                textposition="top center",
                textfont={
                    'size': 12,
                    'color': 'white'
                },
                marker={'size': 8}
            )
        )

        fig = apply_common_chart_features(fig)
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
    Input(component_id='interval-measurement', component_property='n_intervals')
)
def update_current_wind(n):
    return [
        get_current_measurement_card(measurement_name='wind_speed_avg', card_header="Prędkość śr."),
        get_current_measurement_card(measurement_name='wind_speed_avg', card_header="Prędkość śr."),
        get_current_measurement_card(measurement_name='wind_speed_avg', card_header="Prędkość śr.")
    ]


@app.callback(
    Output(component_id='slider-wind', component_property='max'),
    Output(component_id='slider-wind', component_property='marks'),
    Output(component_id='div-slider-wind', component_property='style'),
    Input(component_id='interval-measurement', component_property='n_intervals')
)
def update_slider(n):
    slider_max, slider_marks = get_slider_max_and_marks()
    slider_container_display = get_slider_container_display()
    return slider_max, slider_marks, slider_container_display


@app.callback(
    Output('div-timer-wind', 'children'),
    Input('interval-timer', 'n_intervals')
)
def update_timer(n):
    return get_current_date()
