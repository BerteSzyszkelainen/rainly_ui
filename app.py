import locale
import os
from datetime import datetime
import dash
import pandas as pd
import plotly.express as px
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
from utilities.utilities import generate_slider_marks, get_rainfall_sum_per_day

app = dash.Dash(__name__)
locale.setlocale(locale.LC_ALL, 'pl_PL.UTF-8')

BACKGROUND_COLOR = "#5D5C61"
MEASUREMENT_FILE_NAME = "rainfall.csv"

app.layout = html.Div(
    id="root-div",
    children=[
        html.Div(
            id="div-timer",
            children=html.Label(id='label-timer')
        ),
        html.Div(
            id="div-title",
            children=html.Label(id="label-title", children='Rainly')
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

    if not os.path.exists(MEASUREMENT_FILE_NAME) or not os.path.getsize(MEASUREMENT_FILE_NAME):
        return {}, {'display': 'none'}
    else:
        df = get_rainfall_sum_per_day(data_source='rainfall.csv', day_count=day_count)
        fig = px.bar(df,
                     x=df["day"].apply(str) + " " + df["month"].apply(str),
                     y="rainfall",
                     title="Suma opadów / dzień")
        fig.update_layout(yaxis_range=[0, 50])
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

    if not os.path.exists(MEASUREMENT_FILE_NAME) or not os.path.getsize(MEASUREMENT_FILE_NAME):
        return None, {'display': 'none'}
    else:
        df = get_rainfall_sum_per_day(data_source='rainfall.csv', day_count=day_count)
        return 'Suma: {} mm'.format(round(df['rainfall'].sum(), 2)), {'display': 'block'}


@app.callback(
    Output(component_id='div-warning', component_property='style'),
    Input(component_id='interval-measurement', component_property='n_intervals')
)
def update_warning(n):
    if not os.path.exists("rainfall.csv") or not os.path.getsize("rainfall.csv"):
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

    if not os.path.exists(MEASUREMENT_FILE_NAME) or not os.path.getsize(MEASUREMENT_FILE_NAME):
        return None, {}, {'display': 'none'}
    else:
        df = pd.read_csv('rainfall.csv')
        day_count = df['day'].nunique()
        return day_count, generate_slider_marks(day_count), {'display': 'block'}


@app.callback(
    Output('label-timer', 'children'),
    Input('interval-timer', 'n_intervals')
)
def update_timer(n):
    return str(datetime.now().strftime("%A, %#d %B %Y, %H:%M:%S"))


if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0')
