import numpy as np


class Grid:
    """
    This class represents the 30 by 30 grid on which the snake game is played.

    The values veing used in this project are:
    Positions have a default value of 0 to indicate they are empty.
    Positions with a value of 1 represent a part of the snake.
    Positions with a value of 2 represent a food item.

    There is no hard restriction and the values set can be changed because the
    method implementations are generic.
    """

    def __init__(self):
        self.grid = np.reshape([0] * 900, (30, 30))

    def update_pos(self, x, y, val):
        """
        This method updates the value at this grid position to the value passed in.

        Arguments:
            x {int} -- X coordinate in standard coordinate system
            y {int} -- Y coordinate in standard coordinate system
            val  -- The value to set to
        """
        if x >= 0 and x <= 29 and y >= 0 and y <= 29:
            # x and y switched for internal array coordinates
            self.grid[y][x] = val

    def remove_pos(self, x, y):
        """
        This method resets the value at this grid position to the value passed in.

        Arguments:
            x {int} -- X coordinate in standard coordinate system
            y {int} -- Y coordinate in standard coordinate system
        """
        if x >= 0 and x <= 29 and y >= 0 and y <= 29:
            # x and y switched for internal array coordinates
            self.grid[y][x] = 0

    def get_status(self, x, y):
        """
        This method gets the status of the grid at the given position. If it
        returns 1 then the position either has a food item or is empty, and if
        it returns 0, the position is not free because it is either outside the
        boundary or the snake is present at this location.


        Arguments:
            x {int} -- X coordinate in standard coordinate system
            y {int} -- Y coordinate in standard coordinate system

        Returns:
            0 - snake is at this position or the position is outside boundary
            1- This position is empty or has food.

        """
        if x >= 0 and x <= 29 and y >= 0 and y <= 29:
            if self.grid[y][x] != 1:  # x and y switched for internal array coordinates
                return 1
            else:
                return 0
        else:
            return 0
