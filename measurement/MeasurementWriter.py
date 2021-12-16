#!/usr/bin/python3
import csv

class MeasurementWriter:

    def __init__(self, destination_file_path):
        self.destination_file_path = destination_file_path

    def save(self, year, month, day, clock_time, rainfall):

        with open(self.destination_file_path, newline='', mode="a+") as file:
            csv_writer = csv.writer(file, delimiter=',')
            row_to_save = [year, month, day, clock_time, rainfall]
            csv_writer.writerow(row_to_save)

if __name__ == "__main__":
    measurementWriter = MeasurementWriter(destination_file_path=r'C:\Users\szysz\rainly\test\test_rainfall.csv')
    measurementWriter.save(year="2021",
                           month="grudzień",
                           day="16",
                           clock_time="18:00",
                           rainfall="10 mm")
    print("Measurement writer executed successfully.")
