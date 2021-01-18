class Signal:
    """
    This class keeps track of signal traffic lights and it's properties
    """


    def __init__(self, id: int, state:str="red"):
        self.id = id        # id of the signal/ traficlight
        self.state = state  # The state of the traficlight

    def setState(self, value):
        "Set the current state(colour) of the signal traffic light"
        self.state = value
    
    def getState(self):
        return self.state
