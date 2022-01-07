from datetime import datetime
import pandas as pd
import plotly.express as px
import pytz
from babel.dates import format_datetime
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
from utilities.utilities import generate_slider_marks, get_rainfall_sum_per_month, \
    get_rainfall_sum_for_month_for_current_year, month_number_to_name_pl

from app import app

BACKGROUND_COLOR = "#5D5C61"
DATA_SOURCE = r"http://127.0.0.1:5000/get_measurements"


layout = html.Div(
    id="root-div",
    children=[
        html.Div(
            id="div-timer",
            children=html.Label(id='label-timer-monthly-page')
        ),
        html.Div(
            id="div-navigation",
            children=[
                dcc.Link(id='home', children='Start', href='/'),
                dcc.Link(id='home', children='Dzień', href='/apps/daily'),
                dcc.Link(id='home', className="active", children='Miesiąc', href='/apps/monthly'),
                dcc.Link(id='home', children='Rok', href='/apps/yearly')
            ]
        ),
        html.Div(
            id="div-slider-month",
            children=[
                html.Label(id="label-select-range-title", children='Wybierz okres czasu'),
                dcc.Slider(
                    id="slider-month",
                    min=0,
                    value=1,
                )
            ]
        ),
        html.Div(
            id="div-bar-chart-month",
            children=dcc.Loading(children=dcc.Graph(id="bar-chart-month"))
        ),
        html.Div(
            id="div-warning-month",
            children=html.Label(id="label-warning", children="Oczekiwanie na pierwszy pomiar...")
        ),
        html.Div(
            id="div-heatmap-chart-year",
            children=dcc.Loading(children=dcc.Graph(id="heatmap-chart-year"))
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
    Output(component_id='bar-chart-month', component_property='figure'),
    Output(component_id='bar-chart-month', component_property='style'),
    Input(component_id='slider-month', component_property='value'),
    Input(component_id='interval-measurement', component_property='n_intervals')
)
def update_bar_chart(month_count, n):

    df = get_rainfall_sum_per_month(data_source=DATA_SOURCE,
                                  month_count=month_count)

    if df.empty:
        return {}, {'display': 'none'}
    else:
        fig = px.bar(df,
                     x=df["month"].apply(lambda x: month_number_to_name_pl(x)) + " " + df["year"].apply(str),
                     y="rainfall",
                     title=f"Miesiące z wybranego okresu")
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
    Output(component_id='div-warning-month', component_property='style'),
    Input(component_id='interval-measurement', component_property='n_intervals')
)
def update_warning(n):

    df = pd.read_json(DATA_SOURCE)

    if df.empty:
        return {'display': 'block'}


@app.callback(
    Output(component_id='slider-month', component_property='max'),
    Output(component_id='slider-month', component_property='marks'),
    Output(component_id='div-slider-month', component_property='style'),
    Input(component_id='interval-measurement', component_property='n_intervals')
)
def update_slider(n):

    df = pd.read_json(DATA_SOURCE)

    if df.empty:
        return None, {}, {'display': 'none'}
    else:
        month_count = df.groupby(["year", "month"], as_index=False).ngroups
        return month_count, generate_slider_marks(month_count, tick_postfix='m'), {'display': 'block'}


@app.callback(
    Output('label-timer-monthly-page', 'children'),
    Input('interval-timer', 'n_intervals')
)
def update_timer(n):
    return format_datetime(datetime.now(pytz.timezone('Europe/Warsaw')), format="EEEE, d MMMM yyyy, HH:mm:ss", locale='pl')

@app.callback(
    Output(component_id='heatmap-chart-year', component_property='figure'),
    Input(component_id='interval-measurement', component_property='n_intervals')
)
def update_heatmap_chart(n):

    df = get_rainfall_sum_for_month_for_current_year(data_source=DATA_SOURCE)

    fig = px.imshow([df["rainfall"]],
                    labels=dict(x="Miesiąc", y="Rok", color="Opady [mm]"),
                    x=[month_number_to_name_pl(month) for month in df["month"].values.tolist()],
                    y=[df["year"].values.tolist()[0]],
                    color_continuous_scale='blues',
                    title=f"Miesiące w tym roku"
                    )

    fig.update_layout(plot_bgcolor=BACKGROUND_COLOR)
    fig.update_layout(paper_bgcolor=BACKGROUND_COLOR)
    fig.update_layout(font={"color": "white", "size": 18})
    fig.update_layout(xaxis_dtick="n")
    fig.update_layout(yaxis_dtick="n")
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
