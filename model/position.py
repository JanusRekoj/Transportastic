
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
  def __init__(self, lat, lon, dirs, heading, speed, time):
    self.lat = lat
    self.lon = lon
    self.dirs = dirs
    self.heading.heading
    self.speed = speed
    self.time = time

  def parse(self, filepath):
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
 
