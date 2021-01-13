class connectPoint:
    """
    This class keeps track of the connection points between 2 lanes
    it has Location as child
    """
    """
    + connectLocation1
    + connectLocation2

    + method(type): type
    """

    def __init__(self, id: int):
        self.id = id