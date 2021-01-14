import numpy as np

class Location():
    """
    The class is a child of an object and keeps track of what the current lane is and how far it's parent is on the lane.
    """

    
    def __init__(self, id, lane_id: str):
        """
        Sets the parameters for a location. 

        :param id: Unique id to acces this class
        :type str

        :param lane_id: the lane_id of the lane where the location is located.
        :type str
        """
        self.id = id
        self.lane_id = lane_id
        self.meters_from_intersection = 0


    def to_geo(self):
        """
        Returns the coordinates of current location.

        :returns: coordinates of current Location
        :type list
        """
        laneNodes = Lane.self.lane_id.self.Nodes
        distance = 0
        
        for coordinate1, coordinate2 in zip(laneNodes, laneNodes[1:]):
            meters = geodesic(coordinate1, coordinate2)
            distance += meters
            if distance > car_distance:
                meters_to_far = distance - car_distance
                meters_to_car = meters - meters_to_far

                distance_between_coordinates = np.sqrt((coordinate2[0] - coordinate1[0]) ** 2 + (coordinate2[1] - coordinate1[1]) ** 2)
                distance_ratio = meters_to_car / distance_between_coordinates
                lat = coordinate1[0] + distance_ratio * (coordinate2[0] - coordinate1[0])
                lon = coordinate1[1] + distance_ratio * (coordinate2[1] - coordinate1[1])
                return [lat, lon]