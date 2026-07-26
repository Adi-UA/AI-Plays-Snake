import random

from gamesrc.constants import GRID_SIZE
from gamesrc.food import Food
from gamesrc.sensors import cast_food_rays, cast_obstacle_rays


def make_food_decision(snake, food):
    """
    This function returns 3 binary values that tell the snake to either continue
    forward, turn left or turn right based on the food's relative position. If
    the food is behind the snake, the function will ask the snake to turn right.

    Arguments:
        snake {Snake} -- The snake that must make a decision
        food {Food} -- The food the snake is trying to get

    Returns:
        tuple of int -- values of 0 or 1 for go_front, go_left and go_right to indicate
        yes or no for each decision.
    """

    # Find relative distance
    dist_x = food.x - snake.coords[0][0]
    dist_y = food.y - snake.coords[0][1]

    go_front, go_left, go_right = 0, 0, 0

    # Based on distance and orientation make a choice
    if snake.orientation == "U":
        if dist_x == 0:
            if dist_y <= 0:
                go_front = 1
            else:
                go_right = 1
        elif dist_x < 0:
            go_left = 1
        elif dist_x > 0:
            go_right = 1
    elif snake.orientation == "D":
        if dist_x == 0:
            if dist_y <= 0:
                go_right = 1
            else:
                go_front = 1
        elif dist_x < 0:
            go_right = 1
        elif dist_x > 0:
            go_left = 1
    elif snake.orientation == "L":
        if dist_y == 0:
            if dist_x <= 0:
                go_front = 1
            else:
                go_right = 1
        elif dist_y < 0:
            go_right = 1
        elif dist_y > 0:
            go_left = 1
    else:
        if dist_y == 0:
            if dist_y <= 0:
                go_right = 1
            else:
                go_front = 1
        elif dist_y < 0:
            go_left = 1
        elif dist_y > 0:
            go_right = 1

    return go_front, go_left, go_right


def build_inputs(grid, snake, food, mode="legacy"):
    """
    Builds the neural network input vector for the given game state.

    Arguments:
        grid {Grid} -- The grid being used in the game
        snake {Snake} -- The snake being used in the game
        food {Food} -- The food being used in the game
        mode {str} -- "legacy" for the original 11-value binary adjacency
        plus food-direction vector, or "raycast" for the 16-value NERO-style
        directional distance sensors.

    Returns:
        tuple of float -- the input vector for `network.activate`.
    """
    if mode == "legacy":
        adjacent = snake.get_8_adjacent(grid)
        go_front, go_left, go_right = make_food_decision(snake, food)
        return tuple(adjacent + [go_front, go_left, go_right])

    if mode == "raycast":
        obstacle_rays = cast_obstacle_rays(snake)
        food_rays = cast_food_rays(snake, food)
        return tuple(obstacle_rays + food_rays)

    raise ValueError(f"Unknown input mode: {mode!r}")


def generate_food(grid, snake):
    """
    This function generates a Food object ata  random position on the grid such
    that is is not on the snake.

    Arguments:
        grid {Grid} -- The grid where the food must be spawned
        snake {Snake} -- The snake on the grid.

    Returns:
        Food -- The new food object
    """
    while True:
        # Don't want it to be too close to the edge for visual reasons.
        x, y = random.randrange(2, GRID_SIZE - 2), random.randrange(2, GRID_SIZE - 2)
        if (x, y) not in snake.coords:
            return Food(grid, x, y)
