import datetime
import time

def waitFor(interval):
    start_time = time.time()
    while time.time() - start_time <= interval:
        print("Measurement in process...")
        time.sleep(2)

def isWholeHourByMinutes():
    return datetime.datetime.now().minute == 0

def generate_slider_marks(days_count):

    if days_count < 3:
        marks = {i: {'label': '{}d'.format(i), 'style': {'font-size': 25, 'color': 'white'}} for i in range(days_count)}
    elif days_count < 7:
        marks = {i: {'label': '{}d'.format(i), 'style': {'font-size': 25, 'color': 'white'}} for i in [1, 2, 3]}
    elif days_count < 14:
        marks = {i: {'label': '{}d'.format(i), 'style': {'font-size': 25, 'color': 'white'}} for i in [1, 2, 3, 7]}
    elif days_count < 21:
        marks = {i: {'label': '{}d'.format(i), 'style': {'font-size': 25, 'color': 'white'}} for i in [1, 2, 3, 7, 14]}
    elif days_count < 28:
        marks = {i: {'label': '{}d'.format(i), 'style': {'font-size': 25, 'color': 'white'}} for i in [1, 2, 3, 7, 14, 21]}
    else:
        marks = {i: {'label': '{}d'.format(i), 'style': {'font-size': 25, 'color': 'white'}} for i in [1, 2, 3, 7, 14, 21, 28]}

    if days_count < 28:
        marks.update({days_count: {'label': '{}d'.format(days_count), 'style': {'font-size': 25, 'color': 'white'}}})

    return marks
