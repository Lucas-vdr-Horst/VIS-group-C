from .Location import Location
from .SignalManager import SignalManager
import numpy as np

class InductionCoil:
    """
    This class contains the information of an induction coil it's geo positions (GeoShape)
    it has Location as child
    """
    """
    + startLocation
    + endLocation

    + method(type): type
    """
    def __init__(self, coil_id: int, centerLocation: Location, length: float, signalManager : SignalManager = None):
        self.id = coil_id                            # the identifier of the induction coil
        self.centerLocation = centerLocation    # the geo centerlocation of the induction coil
        self.length = length                    # the length of the induction coil for activation
        self.signalManager = None
        
    def get_begin_and_end_locations(self) -> (Location, Location):
        # TODO: make it directional independant
        return (
            Location(self.centerLocation.lane, self.centerLocation.meters_from_intersection - self.length/2),
            Location(self.centerLocation.lane, self.centerLocation.meters_from_intersection + self.length/2),
        )

    #todo make a locationclass
    
    def get_state(self, time) -> bool:
        # TODO: Read status from csv file on given time
        return 

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
    
    
    def convert_distance_to_coordinates(self):
        """
        Convert a specific distance from a coordinateA to a coordinateB to a coordinate.
        """
        begin_node = Location.Lane.self.nodes[-1]
        end_node = Location.Lane.self.nodes[0]

        distance_between_coordinates = np.sqrt((coordinate2[0] - coordinate1[0]) ** 2 + (coordinate2[1] - coordinate1[1]) ** 2)
    
        start_node_sensor, end_node_sensor = InductionCoil.calculate_sensor_point
    
        distance_ratio = start_node_sensor / distance_between_coordinates
        lat = coordinate1[0] + distance_ratio * (coordinate2[0] - coordinate1[0])
        lon = coordinate1[1] + distance_ratio * (coordinate2[1] - coordinate1[1])

        self.sensor_start_coordinates = [lat, lon]
        
        distance_ratio = end_node_sensor / distance_between_coordinates
        lat = coordinate1[0] + distance_ratio * (coordinate2[0] - coordinate1[0])
        lon = coordinate1[1] + distance_ratio * (coordinate2[1] - coordinate1[1])

        self.sensor_end_coordinates - [lat, lon]
    
    def setSignalManager(self, signalMan : SignalManager):
        self.signalManager = signalMan

    def getState(self, time) -> str:
        return self.signalManager.getState(self.id, time) 

    def __repr__(self) -> str:
        return f"<InductionCoil id:{self.id} center:{self.centerLocation} length:{self.length}>"