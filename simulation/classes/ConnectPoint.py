class ConnectPoint:
    """
    This class keeps track of the connection points between 2 lanes
    it has Location as child
    """
    """
    + connectLocation1
    + connectLocation2

    + method(type): type
    """

    def __init__(self, id: str, connectLocation1:[[float]], connectLocation2:[[float]]):
        self.id = id                                # identifier of the connectionpoint (might be obsolete)
        self.connectLocation1 = connectLocation1    # connection point 1 (prefered first node ingress lane)
        self.connectLocation2 = connectLocation2    # connection point 2 (prefered first node exgress lane)

    def type(self):
        return self
