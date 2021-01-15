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

    def __init__(self, id: str, length: int, speed:int, start_posistion, destination):
        self.id = id
        self.length = length
        self.speed = speed
        self.start_position = start_posistion
        self.destination = destination
        self.location = location() # Lane toevoegen

    def move(self):
        """
        The move function is responsible for checking if the car can move forward and updates it's own posistion
        @rtype: object
        """
        # TODO make this function correct
        self.location()

