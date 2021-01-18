from .Location import Location

class Car:
    """
    This class keeps track of properties of a car.
    it has Location as child
    """
    """
    + Location
    + Length
    + Speed

    + method(type): type
    """

    def __init__(self, location: Location, length: int, speed:int, direction: bool):
        self.location = location        # Location object of the car (Lane, meters from intersection)
        self.length = length            # Length of the car
        self.speed = speed              # meters per second
        self.direction = direction      # True == forward || False == Backwards

    def move(self, step_size:float):
        """
        The move function is responsible for checking if the car can move forward and updates it's own posistion
        @step_size is given in miliseconds
        @rtype: object
        """
        # TODO make this function correct
        if self.direction:
            self.location.meters_from_intersection += self.speed * step_size / 1000
        else:
            self.location.meters_from_intersection -= self.speed * step_size / 1000
        

