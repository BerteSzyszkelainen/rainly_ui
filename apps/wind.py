from datetime import datetime
import pandas as pd
import plotly.express as px
import pytz
from babel.dates import format_datetime
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from utilities.utilities import generate_slider_marks, get_rainfall_sum_per_year, get_rainfall_sum_for_each_year, \
    get_rainfall_sum_per_day, month_number_to_name_pl, degrees_to_compass

from app import app

BACKGROUND_COLOR = "#5D5C61"
DATA_SOURCE = r"https://rainly-api.herokuapp.com/get_measurements"


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
                    min=0,
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

    df = pd.read_json(DATA_SOURCE).sort_values(by=['year', 'month', 'day']).iloc[-day_count:]

    if df.empty:
        return {}, {'display': 'none'}
    else:

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df["day"].apply(str) + " " + df["month"].apply(lambda x: month_number_to_name_pl(x)),
                                 y=df["wind_speed_avg"],
                                 name='średnia'))
        fig.add_trace(go.Scatter(x=df["day"].apply(str) + " " + df["month"].apply(lambda x: month_number_to_name_pl(x)),
                                 y=df["wind_speed_max"],
                                 name='maksymalna'))

        fig.update_layout(yaxis_range=[0, 150])
        fig.update_layout(xaxis_title="Dzień")
        fig.update_layout(xaxis_dtick="n")
        fig.update_layout(yaxis_title="km/h")
        fig.update_layout(transition_duration=500)
        fig.update_layout(plot_bgcolor=BACKGROUND_COLOR)
        fig.update_layout(paper_bgcolor=BACKGROUND_COLOR)
        fig.update_traces(marker={'size': 12})
        fig.update_traces(mode='lines+markers')
        fig.update_layout(font={"color": "white", "size": 18})
        fig.update_traces(hovertemplate="Data: %{x}<br>Prędkość wiatru: %{y} km/h")
        fig.update_layout(
            hoverlabel=dict(
                bgcolor='darkseagreen',
                font_size=20,
                font_family="Lucida Console"
            )
        )
        fig.update_layout(
            title="Prędkość wiatru w czasie"
        )
        fig.update_layout(height=400)
        fig.update_layout(margin=dict(l=20, r=20, t=30, b=20))

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
        day_count = df.groupby(["day", "month"], as_index=False).ngroups
        if day_count > 28:
            day_count = 28
        return day_count, generate_slider_marks(day_count, tick_postfix='d'), {'display': 'block'}


@app.callback(
    Output('label-timer-wind', 'children'),
    Input('interval-timer', 'n_intervals')
)
def update_timer(n):
    return format_datetime(datetime.now(pytz.timezone('Europe/Warsaw')), format="EEEE, d MMMM yyyy, HH:mm:ss", locale='pl')