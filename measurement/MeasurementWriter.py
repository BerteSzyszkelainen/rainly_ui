#!/usr/bin/python3
import csv

class MeasurementWriter:

    HEADER = ['date', 'time', 'rainfall']

    def __init__(self, destination_file_path):
        self.destination_file_path = destination_file_path

    def save(self, date, time, rainfall):

        with open(self.destination_file_path, newline='', mode="a") as file:
            csv_writer = csv.writer(file, delimiter=',')
            sniffer = csv.Sniffer()
            has_header = sniffer.has_header(file.read(2048))
            if not has_header:
                csv_writer.write_row(self.HEADER)
            row_to_save = [date, time, rainfall]
            csv_writer.writerow(row_to_save)

if __name__ == "__main__":
    measurementWriter = MeasurementWriter(destination_file_path=r'C:\Users\szysz\rainly\test\test_rainfall.csv')
    date, time, rainfall = '12 grudzień 2021', '13:50:00', '10 mm'
    measurementWriter.save(date=date, time=time, rainfall=rainfall)
    print("Measurement writer executed successfully.")
    print("Data saved, date: {} time: {} rainfall: {}.".format(date, time, rainfall))