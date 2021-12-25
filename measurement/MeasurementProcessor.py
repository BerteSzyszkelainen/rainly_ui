#!/usr/bin/python3
import time
from measurement.MeasurementReader import MeasurementReader
from measurement.MeasurementWriter import MeasurementWriter
from utilities.utilities import isWholeHourByMinutes


class MeasurementProcessor(object):

    def __init__(self):
        pass

    def run(self):
        measurementReader = MeasurementReader(interval=10)
        measurementWriter = MeasurementWriter(destination_file_path=r'/home/pi/Projects/rainly/rainfall.csv')

        while True:
            if isWholeHourByMinutes():
                while True:
                    year, month, day, clock_time, rainfall = measurementReader.read()
                    measurementWriter.save(year=year,
                                           month=month,
                                           day=day,
                                           clock_time=clock_time,
                                           rainfall=rainfall)
            time.sleep(30)

if __name__ == "__main__":
    measurementProcessor = MeasurementProcessor()
    measurementProcessor.run()
    print("Measurement processor executed successfully.")
