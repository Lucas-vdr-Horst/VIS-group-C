class World:
    """
    This class file has access to all other classes in the world
    """
    """
    + Array Cars[]
    + Array Lanes[]
    + Array Signals[]
    + Array InductionCoils[]
    + Time/ticks
    
    + method(type): 
    + stroming -> method that implements the flow/doorstroming of an intersection
    """

    def __init__(self, id: int, n_cars:list, n_lanes:list, n_signals:list, n_inductioncoils:list, runtime: float):
        self.id = id
        self.n_cars = n_cars
        self.n_lanes = n_lanes
        self.n_signal = n_signals
        self.n_inductioncoils = n_inductioncoils
        self.runtime = runtime 

        # runtime is given in double, but can work with dates object of datetime

    def update(self):
        """
        Updates the flow of intersection for the following tick/step
        """
        pass

