from .SignalManager import SignalManager

class Signal:
    """
    This class keeps track of signal traffic lights and it's properties
    """


    def __init__(self, id: int, signalManager : SignalManager = None):
        self.id = id        # id of the signal/ traficlight
        self.signalManager = None
    

    def setSignalManager(self, signalMan : SignalManager):
        self.signalManager = signalMan

    def getState(self, time) -> str:
        return self.signalManager.getState(self.id, time) 
