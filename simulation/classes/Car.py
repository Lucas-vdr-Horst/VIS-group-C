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

    def __init__(self, car_id: str, location: Location, length: int, speed:int, merge_dict:dict=None):
        self.id = car_id
        self.location = location        # Location object of the car (Lane, meters from intersection)
        self.length = length            # Length of the car
        self.speed = speed              # meters per second
        self.merge_dict = merge_dict if merge_dict is not None else {}
        

    def move(self, step_size:float, world):
        """
        The move function is responsible for checking if the car can move forward and updates it's own posistion
        @step_size is given in miliseconds
        @rtype: object
        """
        # TODO make this function correct
        # als locatie meer/minder is dan lane, dan switch (connectie class maken)
        new_meters = self.location.meters_from_intersection + self.speed * step_size / 1000
        if (new_meters > self.location.lane.length) and self.location.lane is not None:
            new_lane = self.location.lane.nextlane
            if new_lane is None:
                return self.location
            new_meters -= self.location.lane.length
            # if new_lane.direction == -1:
            #     new_meters = new_lane.length - new_meters
        else:
            new_lane = self.location.lane
        self.location = Location(new_lane, new_meters)

        # if self.location.lane.direction:
        #     if (self.location.meters_from_intersection + self.speed * step_size / 1000) <= self.location.lane.length: # moving backwards but no to the previeus lane
        #         self.location.meters_from_intersection += self.speed * step_size / 1000
        
        # else:   # moving forwards
        #     if (self.location.meters_from_intersection - self.speed * step_size / 1000) > 0:
        #         self.location.meters_from_intersection -= self.speed * step_size / 1000
        #     else:
        #         if self.location.lane.nextlane == None:
        #             self.location == None
        #         else:
        #             nextlane = self.location.lane.nextlane
        #             self.location = Location(nextlane, nextlane.length-1)
        
        # update the car merge dict
        self.merge_dict['last_time'] = max(self.merge_dict['last_time'], world.runtime+step_size)
        self.merge_dict['first_time'] = min(self.merge_dict['first_time'], world.runtime+step_size)
    
    def declare_merge(self, merge_dict: dict):
        self.merge_dict = merge_dict
    
    def clone(self) -> 'Car':
        return Car(self.id, self.location.clone(), self.length, self.speed, self.merge_dict)
