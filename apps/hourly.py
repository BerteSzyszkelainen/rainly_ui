from datetime import datetime
import pandas as pd
import plotly.express as px
from babel.dates import format_datetime
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
from utilities.utilities import generate_slider_marks, get_rainfall_sum_per_day

from app import app

BACKGROUND_COLOR = "#5D5C61"
DATA_SOURCE = r"https://rainly-api.herokuapp.com/get_measurements"


layout = html.Div(
    id="root-div",
    children=[
        html.Div(
            id="div-timer",
            children=html.Label(id='label-timer-hourly-page')
        ),
        html.Div(
            id="div-navigation",
            children=[
                dcc.Link(id='home', children='Start', href='/'),
                dcc.Link(id='home', className="active", children='Godzinowa analiza', href='/apps/hourly'),
                dcc.Link(id='home', children='Dzienna analiza', href='/apps/daily'),
                dcc.Link(id='home', children='Miesięczna analiza', href='/apps/monthly')
            ]
        ),
        html.Div(
            id="div-bar-chart",
            children=dcc.Graph(id="bar-chart")
        ),
        html.Div(
            id="div-warning",
            children=html.Label(id="label-warning", children="Oczekiwanie na pierwszy pomiar...")
        ),
        html.Div(
            id="div-text",
            children=html.Label(id="label-rainfall-sum-result")
        ),
        html.Div(
            id="div-slider",
            children=[
                html.Label(id="label-select-range-title", children='Wybierz zakres dni'),
                dcc.Slider(
                    id="slider",
                    min=0,
                    value=1,
                )
            ]
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
    Output(component_id='bar-chart', component_property='figure'),
    Output(component_id='bar-chart', component_property='style'),
    Input(component_id='slider', component_property='value'),
    Input(component_id='interval-measurement', component_property='n_intervals')
)
def update_bar_chart(day_count, n):

    df = get_rainfall_sum_per_day(data_source=DATA_SOURCE,
                                  day_count=day_count)

    if df.empty:
        return {}, {'display': 'none'}
    else:
        fig = px.bar(df,
                     x=df["day"].apply(str) + " " + df["month"].apply(lambda row: row[:3]),
                     y="rainfall",
                     title="Suma opadów / dzień")
        fig.update_layout(yaxis_autorange=True)
        fig.update_layout(xaxis_title="Dzień")
        fig.update_layout(xaxis_dtick="n")
        fig.update_layout(yaxis_title="mm")
        fig.update_layout(showlegend=False)
        fig.update_layout(transition_duration=500)
        fig.update_layout(plot_bgcolor=BACKGROUND_COLOR)
        fig.update_layout(paper_bgcolor=BACKGROUND_COLOR)
        fig.update_traces(hovertemplate='Data: %{x} <br>Suma opadów: %{y} mm')
        fig.update_traces(marker_color='#557A95')
        fig.update_layout(font={"color": "white", "size": 20})
        fig.update_layout(
            hoverlabel=dict(
                font_size=32,
                font_family="Lucida Console"
            )
        )
        fig.update_layout(
            title={
                'y': 0.9,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'})
        fig.update_layout(height=400)

        return fig, {'display': 'block'}


@app.callback(
    Output(component_id='label-rainfall-sum-result', component_property='children'),
    Output(component_id='label-rainfall-sum-result', component_property='style'),
    Input(component_id='slider', component_property='value'),
    Input(component_id='interval-measurement', component_property='n_intervals')
)
def update_rainfall_sum(day_count, n):

    df = get_rainfall_sum_per_day(data_source=DATA_SOURCE,
                                  day_count=day_count)

    if df.empty:
        return None, {'display': 'none'}
    else:
        return 'Suma: {} mm'.format(round(df['rainfall'].sum(), 2)), {'display': 'block'}


@app.callback(
    Output(component_id='div-warning', component_property='style'),
    Input(component_id='interval-measurement', component_property='n_intervals')
)
def update_warning(n):

    df = pd.read_json(DATA_SOURCE)

    if df.empty:
        return {'display': 'block'}
    else:
        return {'display': 'none'}


@app.callback(
    Output(component_id='slider', component_property='max'),
    Output(component_id='slider', component_property='marks'),
    Output(component_id='div-slider', component_property='style'),
    Input(component_id='interval-measurement', component_property='n_intervals')
)
def update_slider(n):

    df = pd.read_json(DATA_SOURCE)

    if df.empty:
        return None, {}, {'display': 'none'}
    else:
        day_count = df['day'].nunique()
        return day_count, generate_slider_marks(day_count), {'display': 'block'}


@app.callback(
    Output('label-timer-hourly-page', 'children'),
    Input('interval-timer', 'n_intervals')
)
def update_timer(n):
    return format_datetime(datetime.now(), format="EEEE, dd MMM yyyy, HH:mm:ss", locale='pl')
