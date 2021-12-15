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
                    date, timestamp, rainfall = measurementReader.read()
                    measurementWriter.save(date=date, timestamp=timestamp, rainfall=rainfall)
            time.sleep(30)

if __name__ == "__main__":
    measurementProcessor = MeasurementProcessor()
    measurementProcessor.run()
    print("Measurement processor executed successfully.")
