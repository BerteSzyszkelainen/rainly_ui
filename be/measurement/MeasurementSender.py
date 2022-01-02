#!/usr/bin/python3
import csv
import os
import requests


class MeasurementSender:

    def __init__(self, destination_url):
        self.destination_url = destination_url

    def send(self, year, month, day, clock_time, rainfall):
        requests.post(url=self.destination_url,
                                 data={'year': year,
                                       'month': month,
                                       'day': day,
                                       'clock_time': clock_time,
                                       'rainfall': rainfall})

        print("Successfully sent data!")


if __name__ == "__main__":
    MeasurementSender = MeasurementSender(destination_url=r'http://localhost:5000/add_measurement')
    MeasurementSender.send(year="2021",
                           month="January",
                           day="3",
                           clock_time="18:00",
                           rainfall="10.00")
