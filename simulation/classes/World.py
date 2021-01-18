class World:
    """
    This class file has access to all other classes in the world
    """

    def __init__(self, id: int, n_cars: list, n_lanes: list, n_signals: list, n_inductioncoils: list, runtime: float):
        self.id = id                                # identifier of the world, simulation name
        self.n_cars = n_cars                        # list of cars that are present in the world
        self.n_lanes = n_lanes                      # list of lanes that are present in the world
        self.n_signal = n_signals                   # list of signals that are present in the world
        self.n_inductioncoils = n_inductioncoils    # list of induction coils that are present in the world
        self.runtime = runtime                      # Current time of the world

        # runtime is given in double, but can work with dates object of datetime

    def update(self):
        """
        Updates the flow of intersection for the following tick/step
        """
        for car in self.n_cars:
            car.move()
        pass

    def get_carlocations(self):
        pass
        #return {car.} #TODO finish line of code
