class location:
    """
    The class is a child of an object and keeps track of what the current lane is and how far it's parent is on the lane.
    """
    """
    + Lane
    + percentage

    + toGeo()
    """
    def __init__(self, id: int):
        self.id = id