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
            children=html.Label(id='label-timer-daily-page')
        ),
        html.Div(
            id="div-navigation",
            children=[
                dcc.Link(id='home', children='Start', href='/'),
                dcc.Link(id='home', children='Godzinowa analiza', href='/apps/hourly'),
                dcc.Link(id='home', className="active", children='Dzienna analiza', href='/apps/daily'),
                dcc.Link(id='home', children='Miesięczna analiza', href='/apps/monthly')
            ]
        ),
        html.Div(
            id="div-heatmap-chart",
            children=dcc.Graph(id="heatmap-chart")
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
def update_bar_chart(n):

    fig = px.imshow([[1, 20, 30],
                     [20, 1, 60],
                     [30, 60, 1]])

    fig.update_layout(plot_bgcolor=BACKGROUND_COLOR)
    fig.update_layout(paper_bgcolor=BACKGROUND_COLOR)
    fig.update_layout(font={"color": "white", "size": 20})
    fig.update_layout(
        hoverlabel=dict(
            font_size=32,
            font_family="Lucida Console"
        )
    )

    return fig


@app.callback(
    Output('label-timer-daily-page', 'children'),
    Input('interval-timer', 'n_intervals')
)
def update_timer(n):
    return format_datetime(datetime.now(), format="EEEE, dd MMM yyyy, HH:mm:ss", locale='pl')