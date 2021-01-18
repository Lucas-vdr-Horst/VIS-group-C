class Signal:
    """
    This class keeps track of signal traffic lights and it's properties
    """
    """
    + field: type
    
    + method(type): type
    """

    def __init__(self, id: int, state:"rood"):
        self.id = id
        self.state = state

    def setState(self, value):
        "Set the current state(colour) of the signal traffic light"
        self.state = value
    
    def getState(self):
        return state
