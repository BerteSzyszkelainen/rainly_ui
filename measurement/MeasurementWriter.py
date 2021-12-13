#!/usr/bin/python3
import csv

class MeasurementWriter:

    def __init__(self, destination_file_path):
        self.destination_file_path = destination_file_path

    def save(self, time, measurement):
        with open(self.destination_file_path, newline='', mode="a") as file:
            csv_writer = csv.writer(file, delimiter=',')
            row_to_save = [time, measurement]
            csv_writer.writerow(row_to_save)

if __name__ == "__main__":
    measurementSaver = MeasurementWriter(destination_file_path=r'C:\Users\szysz\rainly\test\test_rainfall.csv')
    measurementSaver.save(time='2021-12-13 13:50:00', measurement='10 mm')