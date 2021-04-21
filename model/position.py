
from abc import ABC, abstractmethod

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
    pass
    
class Station(Position):
    pass
 
