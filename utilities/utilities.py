from datetime import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd


def generate_slider_marks(days_count, tick_postfix):
    style = {'font-size': 20, 'color': 'white'}
    if days_count < 3:
        marks = {i: {'label': '{}{}'.format(i, tick_postfix), 'style': style} for i in
                 range(1, days_count)}
    elif days_count < 7:
        marks = {i: {'label': '{}{}'.format(i, tick_postfix), 'style': style} for i in
                 [1, 2, 3]}
    elif days_count < 14:
        marks = {i: {'label': '{}{}'.format(i, tick_postfix), 'style': style} for i in
                 [1, 2, 3, 7]}
    elif days_count < 21:
        marks = {i: {'label': '{}{}'.format(i, tick_postfix), 'style': style} for i in
                 [1, 2, 3, 7, 14]}
    elif days_count < 28:
        marks = {i: {'label': '{}{}'.format(i, tick_postfix), 'style': style} for i in
                 [1, 2, 3, 7, 14, 21]}
    else:
        marks = {i: {'label': '{}{}'.format(i, tick_postfix), 'style': style} for i in
                 [1, 2, 3, 7, 14, 21, 28]}

    if days_count < 28:
        marks.update({days_count: {'label': '{}{}'.format(days_count, tick_postfix),
                                   'style': {'font-size': 25, 'color': 'white'}}})

    return marks


def get_rainfall_sum_per_day(data_source, day_count):
    df = pd.read_json(data_source)
    start_date = (datetime.now() - relativedelta(days=day_count-1))\
        .replace(hour=0,
                 minute=0,
                 second=0,
                 microsecond=0)
    df = df.loc[df['date'] > start_date]
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.strftime('%m')
    df['day'] = df['date'].dt.strftime('%d')
    df_sum_per_day = df.groupby(["year", "month", "day"]).sum().reset_index()
    df_sum_per_day = df_sum_per_day.sort_values(by=["year", "month", "day"])
    return df_sum_per_day


def get_rainfall_sum(data_source, day_count):
    df = pd.read_json(data_source)
    start_date = (datetime.now() - relativedelta(days=day_count-1))\
        .replace(hour=0,
                 minute=0,
                 second=0,
                 microsecond=0)
    df = df.loc[df['date'] > start_date]
    rainfall_sum = df['rainfall'].sum()
    return rainfall_sum


def degrees_to_compass(degrees):
    val = int((degrees / 22.5) + .5)
    arr = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
    return arr[(val % 16)]


def get_measurements(data_source, days):
    df = pd.read_json(data_source)
    start_date = (datetime.now() - relativedelta(days=days-1))\
        .replace(hour=0,
                 minute=0,
                 second=0,
                 microsecond=0)
    df = df.loc[df['date'] > start_date]
    df = df.sort_values(by=['date'])
    return df


def apply_common_chart_features(fig):
    BACKGROUND_COLOR = "#5D5C61"
    fig.update_layout(xaxis_title='Dzień')
    fig.update_layout(
        xaxis=dict(
            tickfont=dict(size=12),
        automargin=True,
        tickangle=45))
    fig.update_layout(
        yaxis=dict(
            tickfont=dict(size=12)))
    fig.update_layout(xaxis_dtick="n")
    fig.update_layout(showlegend=False)
    fig.update_layout(transition_duration=500)
    fig.update_layout(plot_bgcolor=BACKGROUND_COLOR)
    fig.update_layout(paper_bgcolor=BACKGROUND_COLOR)
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
    fig.update_layout(height=500)

    return  fig

def apply_common_line_chart_features(fig):
    fig.update_traces(marker={'size': 8})
    fig.update_traces(mode='lines+markers')

    return fig