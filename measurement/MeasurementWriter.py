#!/usr/bin/python3
import csv
import os


class MeasurementWriter:

    HEADER_ROW = ["year","month","day","clock_time","rainfall"]

    def __init__(self, destination_file_path):
        self.destination_file_path = destination_file_path

    def save(self, year, month, day, clock_time, rainfall):

        with open(self.destination_file_path, newline='', mode="a+") as file:
            csv_writer = csv.writer(file, delimiter=',')

            if os.path.getsize(self.destination_file_path) == 0:
                csv_writer.writerow(self.HEADER_ROW)

            row_to_save = [year, month, day, clock_time, rainfall]
            csv_writer.writerow(row_to_save)

        print("Successfully saved data.")

if __name__ == "__main__":
    measurementWriter = MeasurementWriter(destination_file_path=r'C:\Users\szysz\rainly\test_rainfall.csv')
    measurementWriter.save(year="2021",
                           month="grudnia",
                           day="16",
                           clock_time="18:00",
                           rainfall="10 mm")
