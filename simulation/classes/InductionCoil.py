from .Location import Location


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
    def __init__(self, id: int, centerLocation, lengte, state:bool):
        self.id = id
        self.centerLocation = centerLocation
        self.lengte = lengte
        self.state = state

    def setStartAndEndLocation(self):
        # todo
        #centerGeo = get geo # Get from dict from @Freek
        #length = Get length / 2 #Get length of coil from @Freek
        #stoplineGeo = lane.getStoplineGeo()
        #distance_from_stopline = calculateBetween2Points(lat1: centerGeo[0], lon1: centerGeo[1], lat2: stoplineGeo[0],lon1 : stoplineGeo[1])
        #self.start_location = distance_from_stopline - length
        #self.end_location = distance_from_stopline + length
        pass

    #todo make a locationclass

    def setState(self, value):
        'Set state to given values (True/False)'
        self.state = value
        
    
    def getState(self):
        return self.state

    def calculate_sensor_point(self):
        lane_id = Location.self.lane_id
        
        length_to_sides = self.lengte / 2

        begin_node = Location.Lane.self.nodes[0]

        distance_between_coordinates = np.sqrt((self.centerLocation[0]-begin_node[0])**2 + (self.centerLocation[1]-begin_node[1]))
        induction_start_point_meters = distance_between_coordinates - length_to_sides
        induction_end_point_meters = distance_between_coordinates + length_to_sides
        self.induction_start_point_meters = 
        
        return [induction_start_point_meters, induction_end_point_meters]
    
    
    def convert_distance_to_coordinates(self):
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