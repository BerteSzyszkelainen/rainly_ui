import locale
from datetime import datetime

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

app = dash.Dash(__name__)
locale.setlocale(locale.LC_ALL, 'pl_PL.UTF-8')

df = pd.read_csv('rainfall.csv')

app.layout = html.Div(children=[

    html.H3(id='timer', style={'text-align': 'right'}),
    dcc.Interval(
        id='interval-component',
        interval=1 * 1000,
        n_intervals=0
    ),
    html.H1(children='Rainly',
            style={
                'textAlign': 'center',
            }
    ),
    html.Div(children=[
        dcc.Graph(id='daily-rainfall', style={'width': '50%', 'height': '50%', 'display': 'inline-block'}),
        html.H3(id='daily-rainfall-sum', style={'width': '50%', 'height': '50%', 'display': 'inline-block', 'text-align': 'center'})
    ]),
    html.Label('Wybierz zakres dni', style={'font-size': '20px'}),
    dcc.Slider(
        id='daily-rainfall-slider',
        min=1,
        max=28,
        step=None,
        marks={
            1: '1d',
            3: '3d',
            7: '7d',
            14: '14d',
            21: '21d',
            28: '28d'
        },
        value=1,
    ),
    html.Div(children=[
        dcc.Graph(id='monthly-rainfall', style={'width': '50%', 'height': '50%', 'display': 'inline-block'}),
        html.H3(id='monthly-rainfall-sum', style={'width': '50%', 'height': '50%', 'display': 'inline-block', 'text-align': 'center'})
    ]),
    html.Label('Wybierz zakres miesięcy', style={'font-size': '20px'}),
    dcc.RangeSlider(
        id='monthly-rainfall-range-slider',
        min=0,
        max=11,
        step=None,
        marks={
            0: 'styczeń',
            1: 'luty',
            2: 'marzec',
            3: 'kwiecień',
            4: 'maj',
            5: 'czerwiec',
            6: 'lipiec',
            7: 'sierpień',
            8: 'wrzesień',
            9: 'październik',
            10: 'listopad',
            11: 'grudzień'
        },
        value=[0, 1],
    )

])

@app.callback(
    Output('daily-rainfall', 'figure'),
    Input('daily-rainfall-slider', 'value')
)
def update_daily_rainfall_figure(selected_time_range):
    filtered_df = df.iloc[-selected_time_range:]
    fig = px.bar(filtered_df,
                 x='time',
                 y='rainfall',
                 color='color',
                 title="Suma opadów / dzień")
    fig.update_layout(yaxis_range=[0, 20])
    fig.update_layout(xaxis_title="Dzień")
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
    filtered_df = df.iloc[-selected_time_range:]
    return 'Suma opadów / wybrany okres: {} mm'.format(filtered_df['rainfall'].sum())

@app.callback(
    Output('monthly-rainfall', 'figure'),
    Input('monthly-rainfall-range-slider', 'value')
)
def update_monthly_rainfall_figure(selected_time_range):
    df_month = df['time'].str.split('.', expand=True)[1]
    tmpDF = pd.concat([df_month, df['rainfall']], axis=1, keys=["month", "rainfall"])

    tmpDF = tmpDF.groupby(['month'], as_index=False)["rainfall"].sum()
    tmpDF = tmpDF.replace({'01': 'styczeń',
                           '02': 'luty',
                           '03': 'marzec',
                           '04': 'kwiecień',
                           '05': 'maj',
                           '06': 'czerwiec',
                           '07': 'lipiec',
                           '08': 'sierpień',
                           '09': 'wrzesień',
                           '10': 'październik',
                           '11': 'listopad',
                           '12': 'grudzień',
                           })
    filtered_df = tmpDF.iloc[selected_time_range[0]:selected_time_range[1]+1]

    fig = px.bar(filtered_df,
                 x='month',
                 y='rainfall',
                 title="Suma opadów / miesiąc",
                 )
    fig.update_layout(yaxis_range=[0, 200])
    fig.update_layout(xaxis_title="Miesiąc")
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
    Output(component_id='monthly-rainfall-sum', component_property='children'),
    Input(component_id='monthly-rainfall-range-slider', component_property='value')
)
def update_monthly_rainfall_sum(selected_time_range):
    df_month = df['time'].str.split('.', expand=True)[1]
    tmpDF = pd.concat([df_month, df['rainfall']], axis=1, keys=["month", "rainfall"])

    tmpDF = tmpDF.groupby(['month'], as_index=False)["rainfall"].sum()
    tmpDF = tmpDF.replace({'01': 'styczeń',
                           '02': 'luty',
                           '03': 'marzec',
                           '04': 'kwiecień',
                           '05': 'maj',
                           '06': 'czerwiec',
                           '07': 'lipiec',
                           '08': 'sierpień',
                           '09': 'wrzesień',
                           '10': 'październik',
                           '11': 'listopad',
                           '12': 'grudzień',
                           })
    filtered_df = tmpDF.iloc[selected_time_range[0]:selected_time_range[1] + 1]
    return 'Suma opadów / wybrany okres: {} mm'.format(filtered_df['rainfall'].sum())

@app.callback(Output('timer', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_timer(n):
      return str(datetime.now().strftime("%A, %#d %B %Y, %H:%M:%S"))

if __name__ == '__main__':
    app.run_server(debug=True)