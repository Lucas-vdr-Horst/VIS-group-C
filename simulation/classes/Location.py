import numpy as np
from geopy.distance import geodesic
from .Lane import Lane


class Location:
    """
    The class is a child of an object and keeps track of what the current lane is and how far it's parent is on the lane.
    """

    def __init__(self, lane: Lane, meters_from_intersection: float):
        """
        Sets the parameters for a location. 

        :param id: Unique id to acces this class
        :type str

        :param lane_id: the lane_id of the lane where the location is located.
        :type str
        """
        self.lane = lane                                            # Lane object
        self.meters_from_intersection = meters_from_intersection    # Meters from intersection
    
    def to_geo(self) -> (float, float):
        distance = 0
        for i in range(len(self.lane.nodes)-1):
            current_node = self.lane.nodes[i]
            next_node = self.lane.nodes[i+1]
            add_distance = geodesic(current_node, next_node).meters
            if distance + add_distance > self.meters_from_intersection:
                weight_shift = (self.meters_from_intersection - distance) / add_distance
                return np.array(current_node) * (1-weight_shift) + np.array(next_node) * weight_shift
            distance += add_distance
        if distance == self.lane.length:
            return self.lane.nodes[-1]
        raise Exception('Meters from intersection outside lane')

    def __repr__(self) -> str:
        return f"<Location lane:{self.lane}, meters:{self.meters_from_intersection}>"

    def __add__(self, other):
        if type(other) in {int, float}:
            return Location(self.lane, self.meters_from_intersection+other)

    def __sub__(self, other):
        if type(other) in {int, float}:
            return self.__add__(-other)

    def clone(self) -> 'Location':
        return Location(self.lane, self.meters_from_intersection)
