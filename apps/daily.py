from datetime import datetime
import pandas as pd
import plotly.express as px
import pytz
from babel.dates import format_datetime
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
from utilities.utilities import generate_slider_marks, get_rainfall_sum_per_day, \
    get_rainfall_sum_for_day_for_current_month

from app import app

BACKGROUND_COLOR = "#5D5C61"
DATA_SOURCE = r"https://rainly-api.herokuapp.com/get_measurements"


layout = html.Div(
    id="root-div",
    children=[
        html.Div(
            id="div-timer",
            children=html.Label(id='label-timer-daily-page')
        ),
        html.Div(
            id="div-navigation",
            children=[
                dcc.Link(id='home', children='Start', href='/'),
                dcc.Link(id='home', className="active", children='Dzień', href='/apps/daily'),
                dcc.Link(id='home', children='Miesiąc', href='/apps/monthly'),
                dcc.Link(id='home', children='Rok', href='/apps/yearly')
            ]
        ),
        html.Div(
            id="div-slider-daily",
            children=[
                html.Label(id="label-select-range-title", children='Wybierz okres czasu'),
                dcc.Slider(
                    id="slider",
                    min=0,
                    value=1,
                )
            ]
        ),
        html.Div(
            id="div-bar-chart-daily",
            children=dcc.Loading(children=dcc.Graph(id="bar-chart-daily"))
        ),
        html.Div(
            id="div-warning-daily",
            children=html.Label(id="label-warning-daily", children="Oczekiwanie na pierwszy pomiar...")
        ),
        html.Div(
            id="div-heatmap-chart-month",
            children=dcc.Loading(children=dcc.Graph(id="heatmap-chart-month"))
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
    Output(component_id='bar-chart-daily', component_property='figure'),
    Output(component_id='bar-chart-daily', component_property='style'),
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
                     x=df["day"].apply(str) + " " + df["month"],
                     y=df["rainfall"],
                     title=f"Dni z wybranego okresu")
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
        fig.update_layout(font={"color": "white", "size": 18})
        fig.update_layout(
            hoverlabel=dict(
                bgcolor='darkseagreen',
                font_size=20,
                font_family="Lucida Console"
            )
        )
        fig.update_layout(
            title={
                'y': 1.0,
                'x': 0.0,
                'xanchor': 'left',
                'yanchor': 'auto'})
        fig.update_layout(height=400)
        fig.update_layout(margin=dict(l=20, r=20, t=30, b=20))

        return fig, {'display': 'block'}


@app.callback(
    Output(component_id='div-warning-daily', component_property='style'),
    Input(component_id='interval-measurement', component_property='n_intervals')
)
def update_warning(n):

    df = pd.read_json(DATA_SOURCE)

    if df.empty:
        return {'display': 'block'}


@app.callback(
    Output(component_id='slider', component_property='max'),
    Output(component_id='slider', component_property='marks'),
    Output(component_id='div-slider-daily', component_property='style'),
    Input(component_id='interval-measurement', component_property='n_intervals')
)
def update_slider(n):

    df = pd.read_json(DATA_SOURCE)

    if df.empty:
        return None, {}, {'display': 'none'}
    else:
        day_count = df['day'].nunique()
        return day_count, generate_slider_marks(day_count, tick_postfix='d'), {'display': 'block'}


@app.callback(
    Output('label-timer-daily-page', 'children'),
    Input('interval-timer', 'n_intervals')
)
def update_timer(n):
    return format_datetime(datetime.now(pytz.timezone('Europe/Warsaw')), format="EEEE, d MMMM yyyy, HH:mm:ss", locale='pl')

@app.callback(
    Output(component_id='heatmap-chart-month', component_property='figure'),
    Input(component_id='interval-measurement', component_property='n_intervals')
)
def update_heatmap_chart(n):

    df = get_rainfall_sum_for_day_for_current_month(data_source=DATA_SOURCE)

    fig = px.imshow([df["rainfall"].values.tolist()],
                    labels=dict(x="Dzień", y="Miesiąc", color="Opady [mm]"),
                    x=df["day"].values.tolist(),
                    y=[df["month"].values.tolist()[0]],
                    color_continuous_scale='blues',
                    title=f"Dni w tym miesiącu",
                    aspect="auto"
                    )

    fig.update_layout(plot_bgcolor=BACKGROUND_COLOR)
    fig.update_layout(paper_bgcolor=BACKGROUND_COLOR)
    fig.update_layout(font={"color": "white", "size": 18})
    fig.update_layout(xaxis_dtick="n")
    fig.update_layout(
        hoverlabel=dict(
            bgcolor='darkseagreen',
            font_size=20,
            font_family="Lucida Console"
        )
    ),
    fig.update_layout(
        title={
            'y': 1.0,
            'x': 0.0,
            'xanchor': 'left',
            'yanchor': 'auto'})
    fig.update_layout(margin=dict(l=20, r=20, t=30, b=20))

    return fig
