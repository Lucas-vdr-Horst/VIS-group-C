from .Signal import Signal
from geopy.distance import geodesic


class Lane:
    """
    This class contains information of what nodes are pressent on that lane, what connectionpoint there are and if there are signal lights
    """
    
    def __init__(self, id: str, nodes: tuple, type_lane:str, signal: Signal=None):
        self.id = id                    # Lane identifier
        self.nodes = nodes              # Geo codes from the lane (lat, lon)
        self.signal = signal            # Signal lights from tracfic lights
        self.length = sum([geodesic(nodes[i], nodes[i+1]).meters for i in range(len(nodes)-1)]) # Calculate length of the lane
        self.type_lane = type_lane      # Ingress, Trajectory, Exgress
        
    def check_trafficlight(self):
        """
        Check the state of the traffic light. If the signal is on red, the car cannot move to the next lane ( Ingress -> trajectory -> Exgress)
        """
        return self.signal.getState()
    
    def getNodes(self):
        return self.nodes
    
    def getFirstNodes(self):
        return self.nodes[0]
    def getTypeLane(self):
        return self.type_lane

    def car_inductioncoil(self):
        "Calculate whether a car is driving over a induction loop"
        pass

    def setConnectionPoints(self, connection_points):
        self.connectpoints = connection_points
    
    def setInductionloop(self, value):
        self.inductioncoils.append(value)
