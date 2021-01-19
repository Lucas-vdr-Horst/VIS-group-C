from copy import copy
from .Car import Car

class World:
    """
    This class file has access to all other classes in the world
    """

    def __init__(self, cars: list, lanes: list, signals: list, induction_coils: list, runtime: float):
        self.cars = cars                        # list of cars that are present in the world
        self.lanes = lanes                      # list of lanes that are present in the world
        self.signals = signals                   # list of signals that are present in the world
        self.induction_coils = induction_coils    # list of induction coils that are present in the world
        self.runtime = runtime                      # Current time of the world

        # runtime is given in double, but can work with dates object of datetime

    def clone(self) -> 'World':
        cars = [Car(r.id, copy(r.location), r.length, r.speed, r.direction) for r in self.cars]
        clone = World(cars, self.lanes, self.signals, self.induction_coils, self.runtime)
        return clone

    def update(self, step_size: float) -> 'World':
        """
        Updates the flow of intersection for the following tick/step,
        Stepsize can be negative
        """
        new_world = self.clone()
        for car in new_world.cars:
            car.move(step_size, new_world)
        return new_world

    def get_carlocations(self) -> dict:
        return {car.id : car.to_geo() for car in self.cars}

    def get_induction_coil_states(self) -> dict:
        return {induction_coil.id: induction_coil.get_state(self.runtime) for induction_coil in self.induction_coils}
