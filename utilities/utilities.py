import pandas as pd

def generate_slider_marks(days_count):
    if days_count < 3:
        marks = {i: {'label': '{}d'.format(i), 'style': {'font-size': 25, 'color': 'white'}} for i in
                 range(1, days_count)}
    elif days_count < 7:
        marks = {i: {'label': '{}d'.format(i), 'style': {'font-size': 25, 'color': 'white'}} for i in [1, 2, 3]}
    elif days_count < 14:
        marks = {i: {'label': '{}d'.format(i), 'style': {'font-size': 25, 'color': 'white'}} for i in [1, 2, 3, 7]}
    elif days_count < 21:
        marks = {i: {'label': '{}d'.format(i), 'style': {'font-size': 25, 'color': 'white'}} for i in [1, 2, 3, 7, 14]}
    elif days_count < 28:
        marks = {i: {'label': '{}d'.format(i), 'style': {'font-size': 25, 'color': 'white'}} for i in
                 [1, 2, 3, 7, 14, 21]}
    else:
        marks = {i: {'label': '{}d'.format(i), 'style': {'font-size': 25, 'color': 'white'}} for i in
                 [1, 2, 3, 7, 14, 21, 28]}

    if days_count < 28:
        marks.update({days_count: {'label': '{}d'.format(days_count), 'style': {'font-size': 25, 'color': 'white'}}})

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

def get_rainfall_sum_for_day_for_current_month(data_source):
    df = pd.read_json(data_source)
    df = df.loc[(df['month'] == "Styczeń") & (df['year'] == 2022)]
    df_sum_per_day = df.groupby(["day", "month", "rainfall"], as_index=False) \
        .sum() \
        .sort_values(by=['day'])
    return df_sum_per_day
