from .Location import Location

from .SignalManager import SignalManager
import numpy as np


class InductionCoil:
    """
    This class contains the information of an induction coil it's poistion on the lane
    it has Location as child
    """

    def __init__(self, coil_id: int, centerLocation: Location, length: float, signalManager : SignalManager = None, intersection : str = None):
        self.id = coil_id                            # the identifier of the induction coil
        self.centerLocation = centerLocation         # the geo centerlocation of the induction coil
        self.length = length                         # the length of the induction coil for activation
        self.signalManager = None                    # the signal manager of this class
        self.intersection = None                     # the intersection name
        
    
    def get_begin_and_end_locations(self) -> (Location, Location):
        return (
            Location(self.centerLocation.lane, self.centerLocation.meters_from_intersection - self.length/2),
            Location(self.centerLocation.lane, self.centerLocation.meters_from_intersection + self.length/2),
        )
    
      
    def calculate_sensor_point(self):
        """
        This function calculates the distance between the beginnode of 
        a lane and the beginpoint of a sensor and the distance between 
        the beginnode of a lane and the endpoint of a sensor.

        :returns: distance between stopline and beginpoint sensor and distance between stopline and endpoint sensor
        :type list
        """
        lane_id = Location.self.lane_id
        
        length_to_sides = self.length / 2

        begin_node = Location.Lane.self.nodes[0]

        distance_between_coordinates = np.sqrt((self.centerLocation[0]-begin_node[0])**2 + (self.centerLocation[1]-begin_node[1]))
        induction_start_point_meters = distance_between_coordinates - length_to_sides
        induction_end_point_meters = distance_between_coordinates + length_to_sides
        

        return [induction_start_point_meters, induction_end_point_meters]
    
    # Setters and Getters
    def setIntersection(self, filename : str):
        self.intersection = filename