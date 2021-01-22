from .Car import Car

merge_distance = 3


class World:
    """
    This class file has access to all other classes in the world
    """

    def __init__(self, cars: list, lanes: list, signals: list, induction_coils: list, runtime: float):
        self.cars = {c.id: c for c in cars}    # list of cars that are present in the world
        self.lanes = lanes                      # list of lanes that are present in the world
        self.signals = signals                   # list of signals that are present in the world
        self.induction_coils = induction_coils    # list of induction coils that are present in the world
        self.runtime = runtime                      # Current time of the world

        # runtime is given in double, but can work with dates object of datetime

    def clone(self) -> 'World':
        cars = [r.clone() for r in self.cars.values() if r.location is not None]
        clone = World(cars, self.lanes, self.signals, self.induction_coils, self.runtime)
        return clone

    def next_world(self, step_size: float) -> 'World':
        """
        Updates the flow of intersection for the following tick/step,
        Stepsize can be negative
        """
        new_world = self.clone()
        for car in new_world.cars.values():
            car.move(step_size, new_world)
        new_world.runtime += step_size
        return new_world
    
    def get_car_by_multiple_ids(self, ids: list) -> Car:
        cars = [self.cars.get(i) for i in ids if self.cars.get(i) is not None]
        return cars[0] if len(cars)>0 else None

    def get_carlocations(self) -> dict:
        return {car.id : car.to_geo() for car in self.cars}

    def get_induction_coil_states(self) -> dict:
        return {induction_coil.id: induction_coil.get_state(self.runtime) for induction_coil in self.induction_coils}
    
    def __repr__(self) -> str:
        return f"<World time:{self.runtime}>"

    def __eq__(self, other) -> bool:
        if type(other) is World:
            return self.runtime == other.runtime
        else:
            return False

    def merge_world_into(self, other_world: 'World', car_merges: dict) -> None:
        new_cars_dict = {}
        for car_a in self.cars.values():
            for car_b in other_world.cars.values():
                if car_a.location.lane.id == car_b.location.lane.id \
                        and abs(car_a.location.meters_from_intersection - car_b.location.meters_from_intersection) < merge_distance:
                    for k in car_merges:
                        if car_merges[k] == car_merges[car_b.id]:
                            car_merges[k] = car_a.id
                    del car_b
                else:
                    new_cars_dict[car_b.id] = car_b
                new_cars_dict[car_a.id] = car_a

        self.cars = new_cars_dict
