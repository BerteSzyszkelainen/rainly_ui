import pandas as pd
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from utilities.utilities import get_card
from utilities.utilities import get_card_children
from utilities.utilities import get_last_measurement_time_and_value
from utilities.utilities import get_measurements
from utilities.utilities import add_common_chart_features
from utilities.utilities import read_configuration
from utilities.utilities import get_navigation
from utilities.utilities import get_slider
from utilities.utilities import get_slider_max_and_marks
from utilities.utilities import get_style_display
from utilities.utilities import get_interval_timer
from utilities.utilities import get_warning
from utilities.utilities import get_interval_measurement
from utilities.utilities import get_timer
from utilities.utilities import get_line_chart
from utilities.utilities import get_current_date
import dash_bootstrap_components as dbc
from app import app


CONFIG = read_configuration()
DATA_SOURCE = CONFIG['DATA']['source']


layout = html.Div(
    id="div-root",
    children=[
        get_timer(id_postfix='air-quality'),
        get_navigation(active='Jakość powietrza'),
        html.Div(
            id="div-current-air-quality",
            children=dbc.Row(
                children=[
                    dbc.Col(dbc.Card(get_card(id='current-air-quality-pm-two-five', color='#D39CB6'))),
                    dbc.Col(dbc.Card(get_card(id='current-air-quality-pm-ten', color='#755F91'))),
                ],
                className="mb-5",
                style={"width": "60rem", 'margin': '0 auto', 'float': 'none'}
            )
        ),
        get_slider(id_postfix='air-quality'),
        get_line_chart(id_postfix='air-quality'),
        get_warning(id_postfix='air-quality'),
        get_interval_timer(),
        get_interval_measurement()
    ]
)


@app.callback(
    Output(component_id='div-line-chart-air-quality', component_property='children'),
    Output(component_id='div-line-chart-air-quality', component_property='style'),
    Input(component_id='slider-air-quality', component_property='value'),
    Input(component_id='interval-measurement', component_property='n_intervals')
)
def update_line_chart(day_count, n):
    df = get_measurements(day_count=day_count)

    if df.empty:
        return {}, {'display': 'none'}
    else:
        fig = go.Figure()
        date_format = '%d.%m %H:%M'

        fig.add_trace(
            go.Scatter(
                x=df["date"].dt.strftime(date_format),
                y=df["pm_two_five"],
                name="Cząsteczki PM2.5",
                mode='lines+markers',
                line={'color': '#D39CB6'},
                marker={'size': 8, 'color': ['#D39CB6' for item in df["pm_two_five"]]},
            )
        )

        fig.add_trace(
            go.Scatter(
                x=df["date"].dt.strftime(date_format),
                y=df["pm_ten"],
                name="Cząsteczki PM10.0",
                mode='lines+markers',
                line={'color': '#755F91'},
                marker={'size': 8, 'color': ['#755F91' for item in df["pm_ten"]]},
            )
        )

        fig = add_common_chart_features(fig)
        fig.update_layout(showlegend=True)
        fig.update_layout(yaxis_range=[0, 20])
        fig.update_layout(yaxis_title="mikrogram/m3")
        fig.update_traces(hovertemplate="Data: %{x}<br>%{y} mikrograma/m3 <extra></extra>")

        return dcc.Loading(children=dcc.Graph(figure=fig)), {'display': 'block'}


@app.callback(
    Output(component_id='div-warning-air-quality', component_property='style'),
    Input(component_id='interval-measurement', component_property='n_intervals')
)
def update_warning(n):
    df = pd.read_json(DATA_SOURCE)

    if df.empty:
        return {'display': 'block'}


@app.callback(
    Output(component_id='current-air-quality-pm-two-five', component_property='children'),
    Output(component_id='current-air-quality-pm-ten', component_property='children'),
    Output(component_id='div-current-air-quality', component_property='style'),
    Input(component_id='interval-measurement', component_property='n_intervals')
)
def update_current_air_quality(n):
    time, pm_two_five = get_last_measurement_time_and_value(measurement_name='pm_two_five')
    _, pm_ten = get_last_measurement_time_and_value(measurement_name='pm_ten')
    style_display = get_style_display()
    return [
        get_card_children(
            card_header='Cząsteczki PM2.5',
            card_paragraph=f'{round(pm_two_five, 1)} mikrograma/m3',
            card_footer=f'Czas pomiaru: {time}'
        ),
        get_card_children(
            card_header='Cząsteczki PM10',
            card_paragraph=f'{round(pm_ten, 1)} mikrograma/m3',
            card_footer=f'Czas pomiaru: {time}'
        ),
        style_display
    ]


@app.callback(
    Output(component_id='slider-air-quality', component_property='max'),
    Output(component_id='slider-air-quality', component_property='marks'),
    Output(component_id='div-slider-air-quality', component_property='style'),
    Input(component_id='interval-measurement', component_property='n_intervals')
)
def update_slider(n):
    slider_max, slider_marks = get_slider_max_and_marks()
    slider_container_display = get_style_display()
    return slider_max, slider_marks, slider_container_display


@app.callback(
    Output('div-timer-air-quality', 'children'),
    Input('interval-timer', 'n_intervals')
)
def update_timer(n):
    return get_current_date()
