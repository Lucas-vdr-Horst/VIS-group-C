from .Signal import Signal


class Lane:
    """
    This class contains information of what nodes are pressent on that lane, what connectionpoint there are and if there are signal lights
    """
    """
    + id 
    + Array Nodes [] - list of coordinates(lat, lon) of the lane
    + Maybe Signal
    +Array connectpoints()
    
    + method(type): type
    """

    def __init__(self, id: str,length: int,  nodes, signal: Signal, type_lane):
        self.id = id
        self.nodes = nodes
        self.signal = signal if signal is not None else None 
        self.length = length 
        self.type_lane = type_lane
        
    def checkTrafficlight(self):
        """
        Check the state of the traffic light. Signal uit
        """
        return self.signal.getState()
    
    def getNodes(self):
        return self.nodes

    def car_inductioncoil(self):
        "Calculate whether a car is driving over a induction loop"
        pass

    def setConnectionPoints(self, connection_points):
        self.connectpoints = connection_points
