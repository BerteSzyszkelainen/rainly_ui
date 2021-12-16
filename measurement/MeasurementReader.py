#!/usr/bin/python3
import datetime
import locale
from gpiozero import Button
from utilities import utilities


locale.setlocale(locale.LC_ALL, "pl_PL.UTF-8")


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
        current_timestamp = datetime.datetime.now()
        year = current_timestamp.strftime("%Y")
        month = current_timestamp.strftime("%B")
        day = current_timestamp.strftime("%d")
        clock_time = current_timestamp.strftime("%H:%m")
        utilities.waitFor(interval=self.interval)
        rainfall = self.tip_count * self.BUCKET_SIZE
        self.reset_rainfall()
        return year, month, day, clock_time, round(rainfall, 2)

if __name__ == "__main__":
    measurementReader = MeasurementReader(interval=10)
    year, month, day, clock_time, rainfall = measurementReader.read()
    print("Measurement reader executed successfully.")
    print("year: {} month: {} day: {} clock_time: {} rainfall: {}"
          .format(year, month, day, clock_time, rainfall))
