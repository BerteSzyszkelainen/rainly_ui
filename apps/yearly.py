import random

from babel.dates import format_datetime
from dash import dcc
from dash import html
from datetime import datetime
from dash.dependencies import Input, Output
import plotly.express as px

from app import app

BACKGROUND_COLOR = "#5D5C61"

layout = html.Div(
    id="root-div",
    children=[
        html.Div(
            id="div-timer",
            children=html.Label(id='label-timer-yearly-page')
        ),
        html.Div(
            id="div-navigation",
            children=[
                dcc.Link(id='home', children='Start', href='/'),
                dcc.Link(id='home', children='Godzinowa analiza', href='/apps/daily'),
                dcc.Link(id='home', children='Dzienna analiza', href='/apps/monthly'),
                dcc.Link(id='home', className="active", children='Roczna analiza', href='/apps/yearly')
            ]
        ),
        html.Div(
            id="div-heatmap-chart",
            children=dcc.Graph(id="heatmap-chart-yearly")
        ),
        html.Div(
            id="div-heatmap-chart-2",
            children=dcc.Graph(id="heatmap-chart-yearly-2")
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
    Output(component_id='heatmap-chart-yearly', component_property='figure'),
    Input(component_id='interval-measurement', component_property='n_intervals')
)
def update_heatmap_chart(n):

    rainfall_per_month_per_day = [[round(random.uniform(0, 90), 1) for _ in range(12)],
                                  [round(random.uniform(0, 30), 1) for _ in range(12)],
                                  [round(random.uniform(0, 30), 1) for _ in range(12)],
                                  [round(random.uniform(0, 30), 1) for _ in range(12)],
                                  [round(random.uniform(0, 30), 1) for _ in range(12)],
                                  [round(random.uniform(0, 30), 1) for _ in range(12)],
                                  [round(random.uniform(0, 30), 1) for _ in range(12)],
                                  [round(random.uniform(0, 30), 1) for _ in range(12)],
                                  [round(random.uniform(0, 30), 1) for _ in range(12)],
                                  [round(random.uniform(0, 30), 1) for _ in range(12)],
                                  [round(random.uniform(0, 30), 1) for _ in range(12)],
                                  [round(random.uniform(0, 30), 1) for _ in range(12)],
                                  [round(random.uniform(0, 30), 1) for _ in range(12)]]

    fig = px.imshow(rainfall_per_month_per_day,
                    labels=dict(x="Miesiąc", y="Rok", color="Suma opadów"),
                    y=['2010', '2011', '2012', '2013', '2014', '2015', '2016',
                       '2017', '2018', '2019', '2020', '2021', '2022'],
                    x=['Styczeń', 'Luty', 'Marzec', 'Kwiecień', 'Maj', 'Czerwiec', 'Lipiec', 'Sierpień', 'Wrzesień', 'Październik', 'Listopad', 'Grudzień'],
                    color_continuous_scale='blues',
                    title="Suma opadów każdego miesiąca każdego roku"
                    )

    fig.update_layout(plot_bgcolor=BACKGROUND_COLOR)
    fig.update_layout(paper_bgcolor=BACKGROUND_COLOR)
    fig.update_layout(font={"color": "white", "size": 10})
    fig.update_traces(hovertemplate='Data: %{x} %{y} <br>Suma opadów: %{z} mm')
    fig.update_layout(
        hoverlabel=dict(
            font_size=32,
            font_family="Lucida Console"
        )
    )
    fig.update_layout(margin=dict(l=20, r=20, t=50, b=20))

    return fig

@app.callback(
    Output(component_id='heatmap-chart-yearly-2', component_property='figure'),
    Input(component_id='interval-measurement', component_property='n_intervals')
)
def update_heatmap_chart(n):

    rainfall_sum_per_year = [[round(random.uniform(0, 200), 1) for _ in range(13)]]

    fig = px.imshow(rainfall_sum_per_year,
                    labels=dict(x="Rok", y="", color="Suma opadów"),
                    x=['2010', '2011', '2012', '2013', '2014', '2015', '2016',
                       '2017', '2018', '2019', '2020', '2021', '2022'],
                    y=[""],
                    color_continuous_scale='blues',
                    title="Suma opadów każdego roku"
                    )

    fig.update_layout(plot_bgcolor=BACKGROUND_COLOR)
    fig.update_layout(paper_bgcolor=BACKGROUND_COLOR)
    fig.update_layout(font={"color": "white", "size": 10})
    fig.update_traces(hovertemplate='Rok: %{x} <br>Suma opadów: %{z} mm')
    fig.update_layout(
        hoverlabel=dict(
            font_size=32,
            font_family="Lucida Console"
        )
    )
    fig.update_layout(margin=dict(l=20, r=20, t=20, b=20))

    return fig

@app.callback(
    Output('label-timer-yearly-page', 'children'),
    Input('interval-timer', 'n_intervals')
)
def update_timer(n):
    return format_datetime(datetime.now(), format="EEEE, dd MMM yyyy, HH:mm:ss", locale='pl')