#!/usr/bin/python3
from measurement.MeasurementReader import MeasurementReader
from measurement.MeasurementWriter import MeasurementWriter


class MeasurementProcessor(object):

    def __init__(self):
        pass

    def run(self):
        measurementReader = MeasurementReader(interval=60)
        measurementWriter = MeasurementWriter(destination_file_path=r'C:\Users\szysz\rainly\rainfall.csv')
        time, rainfall = measurementReader.read()
        measurementWriter.save(time=time, measurement=rainfall)

if __name__ == "__main__":
    measurementProcessor = MeasurementProcessor()
    measurementProcessor.run()
    print("Measurement processor executed successfully.")