#!/usr/bin/python3
from measurement.MeasurementReader import MeasurementReader
from measurement.MeasurementWriter import MeasurementWriter
from utilities.utilities import isWholeHourByMinutes


class MeasurementProcessor(object):

    def __init__(self):
        pass

    def run(self):
        measurementReader = MeasurementReader(interval=60)
        measurementWriter = MeasurementWriter(destination_file_path=r'C:\Users\szysz\rainly\rainfall.csv')

        if isWholeHourByMinutes():
            while True:
                date, time, rainfall = measurementReader.read()
                measurementWriter.save(date=date, time=time, rainfall=rainfall)

if __name__ == "__main__":
    measurementProcessor = MeasurementProcessor()
    measurementProcessor.run()
    print("Measurement processor executed successfully.")
