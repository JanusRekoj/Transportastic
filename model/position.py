
from abc import ABC, abstractmethod
import csv

class Position(ABC):

  @abstractmethod
  def getLatLon(self):
    pass
     
  @abstractmethod
  def getXY(self):
    pass
    
  @abstractmethod
  def isDriving(self):
    pass


class GPS(Position):
  def __init__(self):
    self.is_valid = False
    self.latitude = None
    self.lat_dir = None
    self.longitude = None
    self.lon_dir = None
    self.speed_over_ground_knots = None
    self.heading_true_course = None
    self.epoch_ts = None

  def parse(self, filepath):
    colnames = ['date_time','is_valid','latitude','lat_dir','longitude','lon_dir','speed_over_ground_knots','heading_true_course','epoch_ts']
    with open(filepath, mode='r') as csv_file:
      csv_reader = csv.DictReader(csv_file)
      line_count = 0
      for row in csv_reader:
        if line_count == 0:
          print(f'Column names are {", ".join(row)}')
          line_count += 1
        for col in row:
          setattr(self, col, row[col] )
          print(f'\t{col}: {row[col]}')
        line_count += 1
        print(f'Processed {line_count} lines.')

class Station(Position):
  pass
 
