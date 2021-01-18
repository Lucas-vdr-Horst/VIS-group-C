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
        return state
