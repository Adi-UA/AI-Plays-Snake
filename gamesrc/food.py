import pygame


class Food:
    """
    This class represents a food object in the snake game.
    """

    def __init__(self, grid, x, y):
        """
        This function instantiates the Food object.

        Arguments:
            grid {Grid} -- The on which this food item is to be placed.
            x {int} -- X coordinate in the standard coordinate system
            y {int} -- Y coordinate in the standard coordinate system
        """
        self.x = x
        self.y = y
        # Project's convention is to map food as a value of 2 on the grid.
        grid.update_pos(x, y, 2)
