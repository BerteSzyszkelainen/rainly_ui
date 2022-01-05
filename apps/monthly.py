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
            children=html.Label(id='label-timer-monthly-page')
        ),
        html.Div(
            id="div-navigation",
            children=[
                dcc.Link(id='home', children='Start', href='/'),
                dcc.Link(id='home', children='Dzienna analiza', href='/apps/daily'),
                dcc.Link(id='home', className="active", children='Miesięczna analiza', href='/apps/monthly'),
                dcc.Link(id='home', children='Roczna analiza', href='/apps/yearly')
            ]
        ),
        html.Div(
            id="div-heatmap-chart",
            children=dcc.Graph(id="heatmap-chart")
        ),
        html.Div(
            id="div-heatmap-chart-2",
            children=dcc.Graph(id="heatmap-chart-2")
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
    Output(component_id='heatmap-chart', component_property='figure'),
    Input(component_id='interval-measurement', component_property='n_intervals')
)
def update_heatmap_chart(n):

    rainfall_per_month_per_day = [[round(random.uniform(0, 30), 1) for _ in range(31)],
                                  [round(random.uniform(0, 30), 1) for _ in range(31)],
                                  [round(random.uniform(0, 30), 1) for _ in range(31)],
                                  [round(random.uniform(0, 30), 1) for _ in range(31)],
                                  [round(random.uniform(0, 30), 1) for _ in range(31)],
                                  [round(random.uniform(0, 30), 1) for _ in range(31)],
                                  [round(random.uniform(0, 30), 1) for _ in range(31)],
                                  [round(random.uniform(0, 30), 1) for _ in range(31)],
                                  [round(random.uniform(0, 30), 1) for _ in range(31)],
                                  [round(random.uniform(0, 30), 1) for _ in range(31)],
                                  [round(random.uniform(0, 30), 1) for _ in range(31)],
                                  [round(random.uniform(0, 30), 1) for _ in range(31)]]

    fig = px.imshow(rainfall_per_month_per_day,
                    labels=dict(x="Numer dnia", y="Miesiąc", color="Suma opadów"),
                    x=['01', '02', '03', '04', '05', '06', '07',
                       '08', '09', '10', '11', '12', '13', '14',
                       '15', '16', '17', '18', '19', '20', '21',
                       '22', '23', '24', '25', '26', '27', '28',
                       '29', '30', '31'],
                    y=['Styczeń', 'Luty', 'Marzec', 'Kwiecień', 'Maj', 'Czerwiec', 'Lipiec', 'Sierpień', 'Wrzesień', 'Październik', 'Listopad', 'Grudzień'],
                    color_continuous_scale='blues',
                    title="Suma opadów każdego dnia każdego miesiąca"
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
    fig.update_layout(margin=dict(l=20, r=20, t=80, b=20))

    return fig

@app.callback(
    Output(component_id='heatmap-chart-2', component_property='figure'),
    Input(component_id='interval-measurement', component_property='n_intervals')
)
def update_heatmap_chart_2(n):

    rainfall_sum_per_month = [[round(random.uniform(0, 100), 1) for _ in range(12)]]

    fig = px.imshow(rainfall_sum_per_month,
                    labels=dict(x="Miesiąc", y="Rok", color="Suma opadów"),
                    x=['Styczeń', 'Luty', 'Marzec', 'Kwiecień', 'Maj', 'Czerwiec', 'Lipiec', 'Sierpień', 'Wrzesień', 'Październik', 'Listopad', 'Grudzień'],
                    y=['2022'],
                    color_continuous_scale='blues',
                    title="Suma opadów każdego miesiąca"
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
    fig.update_layout(margin=dict(l=20, r=20, t=20, b=20))

    return fig

@app.callback(
    Output('label-timer-monthly-page', 'children'),
    Input('interval-timer', 'n_intervals')
)
def update_timer(n):
    return format_datetime(datetime.now(), format="EEEE, dd MMM yyyy, HH:mm:ss", locale='pl')