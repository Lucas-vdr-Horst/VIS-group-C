class lane:
    """
    This class contains information of what nodes are pressent on that lane, what connectionpoint there are and if there are signal lights
    """
    """
    + Array Nodes []
    + Maybe Signal
    +Array connectpoints()
    
    + method(type): type
    """

    def __init__(self, id: str):
        self.id = id