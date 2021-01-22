from .Location import Location


class Car:
    """
    This class keeps track of properties of a car.
    it has Location as child
    """

    def __init__(self, car_id: str, location: Location, length: float, speed: float):
        self.id = car_id
        self.location = location        # Location object of the car (Lane, meters from intersection)
        self.length = length            # Length of the car
        self.speed = speed              # meters per second

    def move(self, step_size: float, world):
        """
        The move function is responsible for checking if the car can move forward and updates it's own posistion
        @step_size is given in miliseconds
        @rtype: object
        """
        # TODO make this function correct \/
        # als locatie meer/minder is dan lane, dan switch (connectie class maken)
        new_meters = self.location.meters_from_intersection + self.speed * step_size / 1000
        if (new_meters > self.location.lane.length) and self.location.lane is not None:
            new_lane = self.location.lane.nextlane
            if new_lane is None:
                return self.location
            new_meters -= self.location.lane.length
        else:
            new_lane = self.location.lane

        self.location = Location(new_lane, new_meters)

    def clone(self) -> 'Car':
        return Car(self.id, self.location.clone(), self.length, self.speed)
