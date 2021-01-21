from .Signal import Signal
from geopy.distance import geodesic


class Lane:
    """
    This class contains information of what nodes are pressent on that lane, what connectionpoint there are and if there are signal lights
    """
    
    def __init__(self, id: str, nodes: tuple, type_lane:str, signal: Signal=None, nextlane:'Lane'=None):
        self.id = id                    # Lane identifier
        self.nodes = nodes              # Geo codes from the lane (lat, lon)
        self.signal = signal            # Signal lights from tracfic lights
        self.length = sum([geodesic(nodes[i], nodes[i+1]).meters for i in range(len(nodes)-1)]) # Calculate length of the lane
        self.type_lane = type_lane      # Ingress, Trajectory, Exgress
        self.nextlane = nextlane
    
    def check_trafficlight(self):
        """
        Check the state of the traffic light. If the signal is on red, the car cannot move to the next lane ( Ingress -> trajectory -> Exgress)
        """
        return self.signal.getState()
    
    def getID(self): #TODO weet niet of dit klopt
        return self.id
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
    
    # def setInductionloop(self, value):
    #     self.inductioncoils.append(value)

    def coordinate_to_meters(self, coordinate: (float, float)) -> float:
        distance = 0
        for i in range(len(self.nodes)-1):
            current_node = self.nodes[i]
            next_node = self.nodes[i+1]
            add_distance = geodesic(current_node, next_node).meters
            cor_distance = geodesic(current_node, coordinate).meters
            if cor_distance < add_distance:
                return distance + cor_distance
            distance += add_distance
        raise Exception("Coordinate out of range of lane")


    def connectedlane(self, lane: 'Lane'):
        self.nextlane = lane
        

    def __repr__(self) -> str:
        return f"<Lane id:{self.id}>"
