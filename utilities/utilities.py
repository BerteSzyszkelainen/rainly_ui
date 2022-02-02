import configparser
from datetime import datetime
import pytz
from babel.dates import format_datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
import dash_bootstrap_components as dbc
from dash import html, dcc


def read_configuration():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config


CONFIG = read_configuration()
DATA_SOURCE = CONFIG['DATA']['source']
MEASUREMENT_INTERVAL = CONFIG['MEASUREMENT']['interval']


def generate_slider_marks(days_count, tick_postfix):
    style = {'font-size': 20, 'color': 'white'}

    if days_count < 3:
        marks = {i: {'label': '{}{}'.format(i, tick_postfix), 'style': style} for i in range(1, days_count)}
    elif days_count < 7:
        marks = {i: {'label': '{}{}'.format(i, tick_postfix), 'style': style} for i in [1, 2, 3]}
    elif days_count < 14:
        marks = {i: {'label': '{}{}'.format(i, tick_postfix), 'style': style} for i in [1, 2, 3, 7]}
    elif days_count < 21:
        marks = {i: {'label': '{}{}'.format(i, tick_postfix), 'style': style} for i in [1, 2, 3, 7, 14]}
    elif days_count < 28:
        marks = {i: {'label': '{}{}'.format(i, tick_postfix), 'style': style} for i in [1, 2, 3, 7, 14, 21]}
    else:
        marks = {i: {'label': '{}{}'.format(i, tick_postfix), 'style': style} for i in [1, 2, 3, 7, 14, 21, 28]}

    if days_count < 28:
        marks.update({days_count: {'label': '{}{}'.format(days_count, tick_postfix), 'style': style}})

    return marks


def get_rainfall_sum_per_day(day_count):
    df = get_measurements(day_count)
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.strftime('%m')
    df['day'] = df['date'].dt.strftime('%d')
    df_sum_per_day = df.groupby(['year', 'month', 'day']).sum().reset_index()
    df_sum_per_day = df_sum_per_day.sort_values(by=['year', 'month', 'day'])
    return df_sum_per_day


def get_total_rainfall_sum(day_count):
    df = get_measurements(day_count)
    rainfall_sum = round(df['rainfall'].sum(), 2)
    return rainfall_sum


def get_rainfall_sum_24h():
    df = pd.read_json(DATA_SOURCE)
    start_date = datetime.now() - relativedelta(days=1)
    df = df.loc[df['date'] > start_date]
    rainfall_sum = round(df['rainfall'].sum(), 2)
    return rainfall_sum


def degrees_to_compass(degrees):
    val = int((degrees / 22.5) + .5)
    arr = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']
    return arr[(val % 16)]


def get_measurements(day_count):
    df = pd.read_json(DATA_SOURCE)
    start_date = (datetime.now() - relativedelta(days=day_count - 1)) \
        .replace(hour=0,
                 minute=0,
                 second=0,
                 microsecond=0)
    df = df.loc[df['date'] > start_date]
    df = df.sort_values(by='date')
    return df


def add_common_chart_features(fig):
    BACKGROUND_COLOR = '#5D5C61'
    fig.update_layout(xaxis_title='Dzień')
    fig.update_layout(xaxis=dict(tickfont=dict(size=12), automargin=True, tickangle=45))
    fig.update_layout(yaxis=dict(tickfont=dict(size=12)))
    fig.update_layout(xaxis_dtick='n')
    fig.update_layout(showlegend=False)
    fig.update_layout(transition_duration=500)
    fig.update_layout(plot_bgcolor=BACKGROUND_COLOR)
    fig.update_layout(paper_bgcolor=BACKGROUND_COLOR)
    fig.update_layout(font=dict(color='white', size=18))
    fig.update_layout(hoverlabel=dict(bgcolor='darkseagreen', font_size=20, font_family='Lucida Console'))
    fig.update_layout(title=dict(x=0.0, y=1.0, xanchor='left', yanchor='auto'))
    fig.update_layout(height=600)

    return fig


def add_common_line_chart_features(fig):
    fig.update_traces(marker={'size': 8})
    fig.update_traces(mode='lines+markers')
    
    return fig


def get_card_children(card_header, card_paragraph, card_footer):
    card_children = [
        dbc.CardHeader(children=card_header, style={'font-size': '16px', 'padding': '5px', 'color': 'white'}),
        dbc.CardBody(children=card_paragraph, style={'font-size': '31px', 'padding': '5px', 'color': 'white'}),
        dbc.CardFooter(children=card_footer, style={'font-size': '12px', 'padding': '5px', 'color': 'white'})
    ]

    return card_children


def get_card(id, color):
    return dbc.Card(id=id, color=color)


def get_interval_timer():
    return dcc.Interval(id='interval-timer', interval=1 * 1000, n_intervals=0)


def get_interval_measurement():
    return dcc.Interval(id='interval-measurement', interval=int(MEASUREMENT_INTERVAL), n_intervals=0)


def get_navigation(active):
    children = [
        dcc.Link(id='link-home', children='Start', href='/'),
        dcc.Link(id='link-rainfall', children='Opady', href='/apps/rainfall'),
        dcc.Link(id='link-temperature', children='Temperatura', href='/apps/temperature'),
        dcc.Link(id='link-humidity', children='Wilgotność', href='/apps/humidity'),
        dcc.Link(id='link-pressure', children='Ciśnienie', href='/apps/pressure'),
        dcc.Link(id='link-wind', children='Wiatr', href='/apps/wind'),
    ]

    for c in children:
        if c.__getattribute__('children') == active:
            c.__setattr__('className', 'active')
            break

    return html.Div(id='div-navigation', children=children)


def get_slider(id_postfix):
    return \
        html.Div(
            id=f'div-slider-{id_postfix}',
            children=[
                'Wybierz okres czasu',
                dcc.Slider(
                    id=f'slider-{id_postfix}',
                    min=1,
                    value=1,
                )
            ]
        )


def get_last_measurement_time_and_value(measurement_name):
    last_row = pd.read_json(DATA_SOURCE).iloc[-1]
    measurement_time, measurement_value = last_row['date'].strftime('%d.%m, %H:%M'), last_row[measurement_name]
    return measurement_time, measurement_value


def get_slider_max_and_marks():
    df = pd.read_json(DATA_SOURCE)

    if df.empty:
        return None, {}
    else:
        slider_max = df.groupby([df['date'].dt.year, df['date'].dt.month, df['date'].dt.day], as_index=False).ngroups
        if slider_max > 28:
            slider_max = 28
        return slider_max, generate_slider_marks(slider_max, tick_postfix='d')


def get_style_display():
    df = pd.read_json(DATA_SOURCE)

    if df.empty:
        return {'display': 'none'}
    else:
        return {'display': 'block'}


def get_warning(id_postfix):
    return html.Div(id=f'div-warning-{id_postfix}', children='Oczekiwanie na pierwszy pomiar...')


def get_timer(id_postfix):
    return html.Div(id=f'div-timer-{id_postfix}')


def get_line_chart(id_postfix):
    return html.Div(id=f'div-line-chart-{id_postfix}')


def get_current_measurement(id_postfix, card_color):
    return \
        html.Div(
            id=f'div-current-{id_postfix}',
            children=dbc.Card(
                color=card_color,
                id=f'current-{id_postfix}',
                style={"width": "20rem", 'margin': '0 auto', 'float': 'none'},
                className="mb-5",
            )
        )


def get_current_date():
    return \
        format_datetime(
            datetime=datetime.now(pytz.timezone('Europe/Warsaw')),
            format='EEE, d MMMM yyyy, HH:mm:ss', locale='pl'
        )

