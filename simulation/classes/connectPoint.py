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
        self.id = id
        self.connectLocation1 = connectLocation1
        self.connectLocation2 = connectLocation2

    def type(self):
        return self
