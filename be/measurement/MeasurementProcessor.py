#!/usr/bin/python3
from be.measurement.MeasurementReader import MeasurementReader
from be.measurement.MeasurementSender import MeasurementSender


class MeasurementProcessor(object):

    def __init__(self):
        pass

    def run(self):
        measurementReader = MeasurementReader(interval=300)
        measurementSender = MeasurementSender(destination_url=r'http://localhost:5000/add_measurement')

        while True:
            year, month, day, clock_time, rainfall = measurementReader.read()
            measurementSender.send(year=year,
                                   month=month,
                                   day=day,
                                   clock_time=clock_time,
                                   rainfall=rainfall)

if __name__ == "__main__":
    measurementProcessor = MeasurementProcessor()
    measurementProcessor.run()
    print("Measurement processor executed successfully!")
