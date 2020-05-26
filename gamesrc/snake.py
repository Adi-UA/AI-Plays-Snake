import pygame


class Snake:
    """
    This class represents the snake in the game.
    """

    def __init__(self):
        """
        This instantiates the snake for the game. By default this snake will
        spawn facing the right with it's head at (14,15) on a 30 by 30 grid.
        """

        # Represents the snake as a list of coordinates in the order head -->
        # tail
        self.coords = [(14, 15)]
        for i in range(5):
            self.coords.append((self.coords[i][0] - 1, self.coords[i][1]))

        # The set of moves the snake has access to.
        # The DLUR order makes it convinient to cycle through
        self.moves = ["D", "L", "U", "R"]

        # Current orientation and corresponding index in moves
        self.orient_index = 3
        self.orientation = "R"

    def get_8_adjacent(self, grid):
        """
        This method will returns the status of the 8 positions adjacent to the snake's head on
        the given grid.

        Arguments:
           grid {Grid} -- The grid on which this snake is placed

        Returns:
           list -- A list of the 8 adjacent positions on the grid. In the list
           values of 1 and 0 represent occupied and not occupied.

           0 - snake is at this position or the position is outside boundary
           1- This position is empty or has food.
        """
        if self.orientation == "U":
            return self._UD_adj_handle(grid, 1)
        elif self.orientation == "D":
            return self._UD_adj_handle(grid, -1)
        elif self.orientation == "L":
            return self._LR_adj_handle(grid, 1)
        else:
            return self._LR_adj_handle(grid, -1)

    def tick(self, grid):
        """
        This function moves the snake 'ahead' by one position on the grid.

        Arguments:
           grid {Grid} -- The grid on which the snake exists
        """

        # Orientation matters when computing what is 'ahead' from the snake's
        # perpective
        if self.orientation == "U":
            new_head = (self.coords[0][0], self.coords[0][1] - 1)
        elif self.orientation == "D":
            new_head = (self.coords[0][0], self.coords[0][1] + 1)
        elif self.orientation == "L":
            new_head = (self.coords[0][0] - 1, self.coords[0][1])
        else:
            new_head = (self.coords[0][0] + 1, self.coords[0][1])

        # The new head position is added, the old head is a part fo the body and
        # the current tail is removed.
        grid.remove_pos(self.coords[-1][0], self.coords[-1][1])
        self.coords = [new_head] + self.coords[:-1]
        grid.update_pos(new_head[0], new_head[1], 1)

    def move(self, grid, mv):
        """
        This function moves the snake by one space to the left or right. Left and
        right is relative to whichever way the snake is facing.

        Arguments:
              grid {Grid} -- The grid on which the snake is present
              mv {str} -- The direction to move in. 'L' for left and 'R' for right.
              Behaviour undefined for any other input.
        """

        # Moves variable allows us to conveniently cycle between orientations
        if mv == "L":
            if self.orient_index != 0:
                self.orient_index -= 1
            else:
                self.orient_index = 3
        elif mv == "R":
            if self.orient_index != 3:
                self.orient_index += 1
            else:
                self.orient_index = 0

        # turn the snake then move it
        self.orientation = self.moves[self.orient_index]
        self.tick(grid)

    def elongate(self, grid):
        """
        This function elongates the snake by moving its head one block forward.

        Arguments:
            grid {Grid} -- The grid on which the snake is placed.
        """
        old_head = self.coords[0]

        # Add the new head to the list of coordinates representing the snake.
        # The added head is calculated differently based on orientation
        if self.orientation == "U":
            self.coords = [(old_head[0], old_head[1] - 1)] + self.coords
        elif self.orientation == "D":
            self.coords = [(old_head[0], old_head[1] + 1)] + self.coords
        elif self.orientation == "L":
            self.coords = [(old_head[0] - 1, old_head[1])] + self.coords
        elif self.orientation == "R":
            self.coords = [(old_head[0] + 1, old_head[1])] + self.coords

        grid.update_pos(self.coords[0][0], self.coords[0][1], 1)

    def collide(self, food):
        """
        This method checks to see if the head of the snake is colliding with the
        given food object. The idea is other parts of the snake cannot touch the
        food object unless the head has already passed through the food.

        Arguments:
              food {Food} -- The food with which collision is to be checked

        Returns:
              boolean -- True if collision occured and False otherwise
        """
        if food.x == self.coords[0][0] and food.y == self.coords[0][1]:
            return True
        else:
            return False

    def _UD_adj_handle(self, grid, i):
        """
        This function does some relative math to figure out what the 8 adjacent
        positions are for when the snake is oriented upwards or downwards

        Arguments:
              grid {Grid} -- The grid on which the snake is present
              i {int} -- Enter 1 for U orientation and -1 for D.

        Returns:
              list -- The list of 8 adjacent positions. The order is:
              one ahead, two ahead,
              left, left + one ahead, left + two ahead
              right, right + one ahead, right + two ahead
        """
        one = grid.get_status(self.coords[0][0], self.coords[0][1] - i)
        two = grid.get_status(self.coords[0][0], self.coords[0][1] - 2 * i)
        three = grid.get_status(self.coords[0][0] - i, self.coords[0][1])
        four = grid.get_status(self.coords[0][0] - i, self.coords[0][1] - i)
        five = grid.get_status(
            self.coords[0][0] - i,
            self.coords[0][1] - 2 * i)
        six = grid.get_status(self.coords[0][0] + i, self.coords[0][1])
        seven = grid.get_status(self.coords[0][0] + i, self.coords[0][1] - i)
        eight = grid.get_status(
            self.coords[0][0] + i,
            self.coords[0][1] - 2 * i)

        return [one, two, three, four, five, six, seven, eight]

    def _LR_adj_handle(self, grid, i):
        """
        This function does some relative math to figure out what the 8 adjacent
        positions are for when the snake is oriented left or right.

        Arguments:
              grid {Grid} -- The grid on which the snake is present
              y {int} -- Enter 1 for L orientation and -1 for R.

        Returns:
              list -- The list of 8 adjacent positions. The order is:
              one ahead, two ahead,
              left, left + one ahead, left + two ahead
              right, right + one ahead, right + two ahead
        """
        one = grid.get_status(self.coords[0][0] - i, self.coords[0][1])
        two = grid.get_status(self.coords[0][0] - 2 * i, self.coords[0][1])
        three = grid.get_status(self.coords[0][0], self.coords[0][1] + i)
        four = grid.get_status(self.coords[0][0] - i, self.coords[0][1] + i)
        five = grid.get_status(
            self.coords[0][0] - 2 * i,
            self.coords[0][1] + i)
        six = grid.get_status(self.coords[0][0], self.coords[0][1] - i)
        seven = grid.get_status(self.coords[0][0] - i, self.coords[0][1] - i)
        eight = grid.get_status(
            self.coords[0][0] - 2 * i,
            self.coords[0][1] - i)

        return [one, two, three, four, five, six, seven, eight]
