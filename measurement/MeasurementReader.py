#!/usr/bin/python3
import time
from gpiozero import Button
from utilities import utilities


class MeasurementReader(object):

    BUCKET_SIZE = 0.2794

    def __init__(self, interval):
        self.interval = interval
        self.sensor = Button(6)
        self.tip_count = 0
        self.sensor.when_pressed = self.bucket_tipped

    def bucket_tipped(self):
        self.tip_count = self.tip_count + 1

    def reset_rainfall(self):
        self.tip_count = 0

    def read(self):
        utilities.waitFor(interval=self.interval)
        timestamp = time.strftime('"%Y-%m-%d %H:%M:%S')
        rainfall = self.tip_count * self.BUCKET_SIZE
        self.reset_rainfall()
        return timestamp, round(rainfall, 2)

if __name__ == "__main__":
    measurementReader = MeasurementReader(interval=10)
    timestamp, rainfall = measurementReader.read()
    print("Measurement reader executed successfully.")
    print("Data read, timestamp: {} measurement: {}.".format(timestamp, rainfall))
