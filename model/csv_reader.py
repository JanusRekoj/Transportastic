#!/usr/env python3

import csv

if __name__ == "__main__":
  filename = 'file.csv'
  with open(filename, mode='r') as csv_file:
      csv_reader = csv.DictReader(csv_file)
      line_count = 0
      for row in csv_reader:
          if line_count == 0:
              print(f'Column names are {", ".join(row)}')
              line_count += 1
          print(f'\t{row["col1"]} and {row["col2"]} and {row["col3"]}.')
          line_count += 1
      print(f'Processed {line_count} lines.')
