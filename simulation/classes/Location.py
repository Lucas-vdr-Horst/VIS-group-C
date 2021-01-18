import numpy as np
from geopy.distance import geodesic
from .Lane import Lane


class Location():
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
        self.meters_from_intersection = meters_from_intersection    # Meters from intersecotion
    
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
        raise Exception('Meters from intersection outside lane')


    def to_geo_old(self):
        """
        Returns the coordinates of current location of a car.

        source of formula = https://math.stackexchange.com/questions/2045174/how-to-find-a-point-between-two-points-with-given-distance

        :returns: coordinates of current Location
        :type list
        """
        laneNodes = Lane.self.lane_id.self.Nodes
        distance = 0
        
        for coordinate1, coordinate2 in zip(laneNodes, laneNodes[1:]):
            meters = geodesic(coordinate1, coordinate2)
            distance += meters
            if distance > self.car_distance:
                meters_to_far = distance - self.car_distance
                meters_to_car = meters - meters_to_far

                distance_between_coordinates = np.sqrt((coordinate2[0] - coordinate1[0]) ** 2 + (coordinate2[1] - coordinate1[1]) ** 2)
                distance_ratio = meters_to_car / distance_between_coordinates
                lat = coordinate1[0] + distance_ratio * (coordinate2[0] - coordinate1[0])
                lon = coordinate1[1] + distance_ratio * (coordinate2[1] - coordinate1[1])
                return [lat, lon]