from .SignalManager import SignalManager

class Signal:
    """
    This class keeps track of signal traffic lights and it's properties
    """


    def __init__(self, id: int, signalManager : SignalManager = None, intersection : str = None):
        self.id = id        # id of the signal/ traficlight
        self.signalManager = None
        self.intersection = None
    

    def setSignalManager(self, signalMan : SignalManager):
        self.signalManager = signalMan
    
    def setIntersection(self, filename : str):
        self.intersection = filename
    
    def getIntersection(self):
        return self.intersection

    def getState(self, time) -> str:
        return self.signalManager.getState(self.id, time, self.intersection) 
