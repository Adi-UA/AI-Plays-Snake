from gamesrc.constants import GRID_SIZE


def hit_self(snake):
    """
    Checks whether the snake's head occupies the same cell as its own body.

    Arguments:
        snake {Snake} -- The snake whose status is to be checked.

    Returns:
        bool -- True if the head collides with the body.
    """
    x, y = snake.coords[0]
    return (x, y) in snake.coords[1:]


def hit_wall(snake):
    """
    Checks whether the snake's head has left the grid boundary.

    Arguments:
        snake {Snake} -- The snake whose status is to be checked.

    Returns:
        bool -- True if the head is outside the grid.
    """
    x, y = snake.coords[0]
    return x < 0 or x > GRID_SIZE - 1 or y < 0 or y > GRID_SIZE - 1


def has_failed(snake):
    """
    Checks whether the snake has met any fail condition: colliding with its
    own body or leaving the grid boundary.

    Arguments:
        snake {Snake} -- The snake whose status is to be checked.

    Returns:
        bool -- True if a fail condition has been met, False otherwise.
    """
    return hit_self(snake) or hit_wall(snake)
