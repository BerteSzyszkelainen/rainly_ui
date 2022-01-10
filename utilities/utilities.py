from datetime import datetime

import pandas as pd
from babel.dates import format_datetime


def generate_slider_marks(days_count, tick_postfix):
    if days_count < 3:
        marks = {i: {'label': '{}{}'.format(i, tick_postfix), 'style': {'font-size': 25, 'color': 'white'}} for i in
                 range(1, days_count)}
    elif days_count < 7:
        marks = {i: {'label': '{}{}'.format(i, tick_postfix), 'style': {'font-size': 25, 'color': 'white'}} for i in
                 [1, 2, 3]}
    elif days_count < 14:
        marks = {i: {'label': '{}{}'.format(i, tick_postfix), 'style': {'font-size': 25, 'color': 'white'}} for i in
                 [1, 2, 3, 7]}
    elif days_count < 21:
        marks = {i: {'label': '{}{}'.format(i, tick_postfix), 'style': {'font-size': 25, 'color': 'white'}} for i in
                 [1, 2, 3, 7, 14]}
    elif days_count < 28:
        marks = {i: {'label': '{}{}'.format(i, tick_postfix), 'style': {'font-size': 25, 'color': 'white'}} for i in
                 [1, 2, 3, 7, 14, 21]}
    else:
        marks = {i: {'label': '{}{}'.format(i, tick_postfix), 'style': {'font-size': 25, 'color': 'white'}} for i in
                 [1, 2, 3, 7, 14, 21, 28]}

    if days_count < 28:
        marks.update({days_count: {'label': '{}{}'.format(days_count, tick_postfix),
                                   'style': {'font-size': 25, 'color': 'white'}}})

    return marks


def get_rainfall_sum_per_day(data_source, day_count):
    df = pd.read_json(data_source)
    df_sum_per_day = df.groupby(["day", "month", "year"], as_index=False) \
        .sum() \
        .sort_values(by=['year', 'month', 'day'])
    return df_sum_per_day.iloc[-day_count:]


def get_rainfall_sum_per_month(data_source, month_count):
    df = pd.read_json(data_source)
    df_sum_per_day = df.groupby(["month", "year"], as_index=False) \
        .sum() \
        .sort_values(by=['year', 'month'])
    return df_sum_per_day.iloc[-month_count:]


def get_rainfall_sum_per_year(data_source, year_count):
    df = pd.read_json(data_source)
    df_sum_per_year = df.groupby(["year"], as_index=False) \
        .sum() \
        .sort_values(by=['year'])
    return df_sum_per_year.iloc[-year_count:]


def get_rainfall_sum_for_day_for_current_month(data_source):
    df = pd.read_json(data_source)
    df = df.loc[(df['month'] == 1) & (df['year'] == 2022)]
    df_sum_per_day = df.groupby(["day", "month", "year"], as_index=False) \
        .sum() \
        .sort_values(by=['day'])
    return df_sum_per_day


def get_rainfall_sum_for_month_for_current_year(data_source):
    df = pd.read_json(data_source)
    df = df.loc[df['year'] == 2022]
    df_sum_per_month = df.groupby(["month", "year"], as_index=False) \
        .sum() \
        .sort_values(by=['month'])
    return df_sum_per_month


def get_rainfall_sum_for_each_year(data_source):
    df = pd.read_json(data_source)
    df_sum_per_year = df.groupby(["year"], as_index=False) \
        .sum() \
        .sort_values(by=['year'])
    return df_sum_per_year


def month_number_to_name_pl(number):
    return format_datetime(datetime.strptime(str(number), "%m"), format="MMM", locale='pl')


def degrees_to_compass(degrees):
    val = int((degrees / 22.5) + .5)
    arr = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
    return arr[(val % 16)]
