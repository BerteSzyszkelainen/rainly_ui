from datetime import datetime
import pandas as pd
import plotly.express as px
import pytz
from babel.dates import format_datetime
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from utilities.utilities import generate_slider_marks, degrees_to_compass, apply_common_line_chart_features, \
    get_measurements, apply_common_chart_features

from app import app

BACKGROUND_COLOR = "#5D5C61"
DATA_SOURCE = r"http://127.0.0.1:5000/get_measurements"


layout = html.Div(
    id="root-div",
    children=[
        html.Div(
            id="div-timer",
            children=html.Label(id='label-timer-wind')
        ),
        html.Div(
            id="div-navigation",
            children=[
                dcc.Link(id='home', children='Start', href='/'),
                dcc.Link(id='home', children='Opady', href='/apps/rainfall'),
                dcc.Link(id='home', children='Temperatura', href='/apps/temperature'),
                dcc.Link(id='home', children='Wilgotność', href='/apps/humidity'),
                dcc.Link(id='home', children='Ciśnienie', href='/apps/pressure'),
                dcc.Link(id='home', className="active", children='Wiatr', href='/apps/wind'),
                dcc.Link(id='home', children='Moduł analityczny', href='/apps/analysis'),
            ]
        ),
        html.Div(
            id="div-slider-wind",
            children=[
                html.Label(id="label-select-range-title", children='Wybierz okres czasu'),
                dcc.Slider(
                    id="slider-wind",
                    min=1,
                    value=7,
                )
            ]
        ),
        html.Div(
            id="div-bar-polar-chart-wind-avg",
            children=dcc.Loading(children=dcc.Graph(id="bar-polar-chart-wind-avg"))
        ),
        html.Div(
            id="div-bar-polar-chart-wind-max",
            children=dcc.Loading(children=dcc.Graph(id="bar-polar-chart-wind-max"))
        ),
        html.Div(
            id="div-line-chart-wind",
            children=dcc.Loading(children=dcc.Graph(id="line-chart-wind"))
        ),
        html.Div(
            id="div-warning-wind",
            children=html.Label(id="label-warning", children="Oczekiwanie na pierwszy pomiar...")
        ),
        dcc.Interval(
            id='interval-timer',
            interval=1 * 1000,
            n_intervals=0
        ),
        dcc.Interval(
            id='interval-measurement',
            interval=60 * 1000,
            n_intervals=0
        )
])


@app.callback(
    Output(component_id='bar-polar-chart-wind-avg', component_property='figure'),
    Output(component_id='bar-polar-chart-wind-avg', component_property='style'),
    Input(component_id='slider-wind', component_property='value'),
    Input(component_id='interval-measurement', component_property='n_intervals')
)
def update_bar_polar_chart_wind_avg(day_count, n):

    df = pd.read_json(DATA_SOURCE)
    df["wind_direction_compass"] = df["wind_direction"].apply(lambda x: degrees_to_compass(x))
    df = df.groupby(["wind_direction_compass", "wind_speed_avg"]).size().reset_index(name="wind_frequency")

    if df.empty:
        return {}, {'display': 'none'}
    else:
        fig = px.bar_polar(df,
                           r="wind_frequency",
                           theta="wind_direction_compass",
                           color="wind_speed_avg",
                           template="plotly_dark",
                           color_discrete_sequence=px.colors.sequential.Plasma,
                           title="Rozkład kierunków średniej prędkości wiatru",
                           labels={"wind_speed_avg": "Prędkość wiatru (km/h)",
                                   "wind_direction_compass": "Kierunek wiatru",
                                   "wind_frequency": "Krotność wystąpienia pomiaru"})
        fig.update_layout(font={"color": "white", "size": 14})
        fig.update_layout(height=600)
        fig.update_layout(plot_bgcolor=BACKGROUND_COLOR)
        fig.update_layout(paper_bgcolor=BACKGROUND_COLOR)

        return fig, {'display': 'block'}

@app.callback(
    Output(component_id='bar-polar-chart-wind-max', component_property='figure'),
    Output(component_id='bar-polar-chart-wind-max', component_property='style'),
    Input(component_id='slider-wind', component_property='value'),
    Input(component_id='interval-measurement', component_property='n_intervals')
)
def update_bar_polar_chart_wind_max(day_count, n):

    df = pd.read_json(DATA_SOURCE)
    df["wind_direction_compass"] = df["wind_direction"].apply(lambda x: degrees_to_compass(x))
    df = df.groupby(["wind_direction_compass", "wind_speed_max"]).size().reset_index(name="wind_frequency")

    if df.empty:
        return {}, {'display': 'none'}
    else:
        fig = px.bar_polar(df,
                           r="wind_frequency",
                           theta="wind_direction_compass",
                           color="wind_speed_max",
                           template="plotly_dark",
                           color_discrete_sequence=px.colors.sequential.Plasma,
                           title="Rozkład kierunków maksymalnej prędkości wiatru",
                           labels={"wind_speed_max": "Prędkość wiatru (km/h)",
                                   "wind_direction_compass": "Kierunek wiatru",
                                   "wind_frequency": "Krotność wystąpienia pomiaru"}
                           )
        fig.update_layout(font={"color": "white", "size": 14})
        fig.update_layout(height=600)
        fig.update_layout(plot_bgcolor=BACKGROUND_COLOR)
        fig.update_layout(paper_bgcolor=BACKGROUND_COLOR)

        return fig, {'display': 'block'}


@app.callback(
    Output(component_id='line-chart-wind', component_property='figure'),
    Output(component_id='line-chart-wind', component_property='style'),
    Input(component_id='slider-wind', component_property='value'),
    Input(component_id='interval-measurement', component_property='n_intervals')
)
def update_line_chart(day_count, n):

    df = get_measurements(DATA_SOURCE, day_count)

    if df.empty:
        return {}, {'display': 'none'}
    else:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df["date"].dt.strftime('%d.%m %H:%M'), y=df["wind_speed_avg"], name='średnia'))
        fig.add_trace(go.Scatter(x=df["date"].dt.strftime('%d.%m %H:%M'), y=df["wind_speed_max"], name='maksymalna'))
        fig = apply_common_chart_features(fig)
        fig = apply_common_line_chart_features(fig)
        fig.update_layout(yaxis_range=[0, 150])
        fig.update_layout(yaxis_title="km/h")
        fig.update_traces(hovertemplate="Data: %{x}<br>Prędkość wiatru: %{y} km/h")
        fig.update_layout(
            title="Prędkość wiatru w czasie"
        )

        return fig, {'display': 'block'}

@app.callback(
    Output(component_id='div-warning-wind', component_property='style'),
    Input(component_id='interval-measurement', component_property='n_intervals')
)
def update_warning(n):

    df = pd.read_json(DATA_SOURCE)

    if df.empty:
        return {'display': 'block'}


@app.callback(
    Output(component_id='slider-wind', component_property='max'),
    Output(component_id='slider-wind', component_property='marks'),
    Output(component_id='div-slider-wind', component_property='style'),
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
    Output('label-timer-wind', 'children'),
    Input('interval-timer', 'n_intervals')
)
def update_timer(n):
    return format_datetime(datetime.now(pytz.timezone('Europe/Warsaw')), format="EEEE, d MMMM yyyy, HH:mm:ss", locale='pl')