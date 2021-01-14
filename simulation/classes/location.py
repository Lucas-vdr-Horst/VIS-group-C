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
        """TODO Coordinaten ophalen van beginpunt lane en uitrekenen waar die coordinaten + meters van intersection op uitkomt."""
        return self.meters_from_intersection