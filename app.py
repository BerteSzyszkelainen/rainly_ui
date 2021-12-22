import locale
from datetime import datetime

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

from utilities.utilities import generate_slider_marks

app = dash.Dash(__name__)
locale.setlocale(locale.LC_ALL, 'pl_PL.UTF-8')

df = pd.read_csv('rainfall.csv')
df_sum_per_day = df.groupby(["day", "month"], as_index=False).sum()
measured_days_count = df['day'].nunique()

app.layout = html.Div(className="root-div",
    children=[
    html.Div(className="timer-div", children=[
        html.Label(id='timer'),
        dcc.Interval(
            id='interval-component',
            interval=1 * 1000,
            n_intervals=0
        )
    ]),
    html.Div(className="title-div", children=[
        html.Br(),
        html.Br(),
        html.Label(className="title-label", children='Rainly'),
        html.Br(),
        html.Br(),
        html.Br()
    ]),
    html.Div(className="container", children=[
        html.Div(className="graph-div", children=[dcc.Graph(id='daily-rainfall')]),
        html.Div(className="text-div", children=[html.Label(className="label-rainfall-sum", children='Suma opadów / wybrany okres'), html.Label(id='daily-rainfall-sum')]),
    ]),
    html.Div(className="slider-div", children=[
        html.Br(),
        html.Br(),
        html.Label(className="label-select-range", children='Wybierz zakres dni'),
        html.Br(),
        html.Br(),
        dcc.Slider(
            id='daily-rainfall-slider',
            min=1,
            max=measured_days_count,
            step=None,
            marks=generate_slider_marks(measured_days_count),
            value=1,
        )
    ])
])

@app.callback(
    Output('daily-rainfall', 'figure'),
    Input('daily-rainfall-slider', 'value')
)
def update_daily_rainfall_figure(selected_time_range):

    filtered_df = df_sum_per_day.iloc[:selected_time_range]
    filtered_df["full date"] = filtered_df["day"].astype(str) + " " + filtered_df["month"]

    fig = px.bar(filtered_df,
                 x='full date',
                 y='rainfall',
                 title="Suma opadów / dzień")

    fig.update_layout(yaxis_range=[0, 35])
    fig.update_layout(xaxis_title="Dzień")
    fig.update_layout(xaxis_dtick="n")
    fig.update_layout(yaxis_title="mm")
    fig.update_layout(showlegend=False)
    fig.update_layout(transition_duration=500)
    fig.update_layout(
        title={
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'})

    return fig

@app.callback(
    Output(component_id='daily-rainfall-sum', component_property='children'),
    Input(component_id='daily-rainfall-slider', component_property='value')
)
def update_daily_rainfall_sum(selected_time_range):

    filtered_df = df_sum_per_day.iloc[:selected_time_range]

    return [html.Br(), html.Br(), '{} mm'.format(round(filtered_df['rainfall'].sum(), 2))]

@app.callback(Output('timer', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_timer(n):
      return str(datetime.now().strftime("%A, %#d %B %Y, %H:%M:%S"))

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0')
