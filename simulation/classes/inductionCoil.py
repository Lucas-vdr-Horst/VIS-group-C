from location import location 
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
    def __init__(self, id: int, start_location, end_location, state:bool):
        self.id = id
        self.start_location = location()
        self.end_location = location()
        self.state = state
    
    def setState(self, value):
        'Set state to given values (True/False)'
        self.state = value
        
    
    def getState(self):
        return state
