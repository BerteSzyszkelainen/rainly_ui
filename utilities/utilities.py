import datetime
import time

def waitFor(interval):
    start_time = time.time()
    while time.time() - start_time <= interval:
        print("Measurement in process...")
        time.sleep(2)

        time.sleep(secs=2)

def isWholeHourByMinutes():
    return datetime.datetime.now().minute == 0