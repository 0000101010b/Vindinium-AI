class Wall(object):
    """
    A mine object.

    Attributes:
        x (int): the mine position in X.
        y (int): the mine position in Y.
        owner (int): the hero's id that owns this mine.
    """
    def __init__(self, x, y):
        """

        :param x (int): the mine position in X.
        :param y (int): the mine position in Y.

        """
        self.x = x
        self.y = y
        self.owner = None
