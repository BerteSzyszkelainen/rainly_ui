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
    )
])

@app.callback(
    Output('daily-rainfall', 'figure'),
    Input('daily-rainfall-slider', 'value')
)
def update_daily_rainfall_figure(selected_time_range):

    result = df.groupby(["day", "month"], as_index=False).sum()
    filtered_df = result.iloc[:selected_time_range]

    fig = px.bar(filtered_df,
                 x='day',
                 y='rainfall',
                 title="Suma opadów / dzień")
    fig.update_layout(yaxis_range=[0, 20])
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

    tmpDF = pd.DataFrame(df, columns=["day", "month", "rainfall"])
    result = tmpDF.groupby(["day", "month"], as_index=False).sum()

    filtered_df = result.iloc[:selected_time_range]
    return 'Suma opadów / wybrany okres: {} mm'.format(filtered_df['rainfall'].sum())

@app.callback(Output('timer', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_timer(n):
      return str(datetime.now().strftime("%A, %#d %B %Y, %H:%M:%S"))

if __name__ == '__main__':
    app.run_server(debug=True)