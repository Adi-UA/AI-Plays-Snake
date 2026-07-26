"""
Directional distance sensors for the snake's head, following the sensor
design in Stanley, Bryant & Miikkulainen (2005), "Real-Time Neuroevolution
in the NERO Video Game" (IEEE TEVC 9(6), 653-668): each sensor reports a
continuous, normalized distance to a specific object type along a fixed
direction, rather than raw binary occupancy.
"""

from gamesrc.constants import GRID_SIZE

MAX_STEPS = GRID_SIZE - 1

# Compass vectors starting at "up" and going clockwise, one per 45 degrees.
_COMPASS = [
    (0, -1), (1, -1), (1, 0), (1, 1),
    (0, 1), (-1, 1), (-1, 0), (-1, -1),
]

# Index into _COMPASS of the "front" direction for each orientation. A 90
# degree turn is 2 slots in the 8-direction compass.
_ORIENT_OFFSET = {"U": 0, "R": 2, "D": 4, "L": 6}


def _directions_for(orientation):
    """
    Returns the 8 direction vectors relative to the given orientation, in
    the fixed order: front, front-right, right, back-right, back,
    back-left, left, front-left.
    """
    offset = _ORIENT_OFFSET[orientation]
    return [_COMPASS[(offset + i) % 8] for i in range(8)]


def cast_obstacle_rays(snake):
    """
    Casts a ray in each of the 8 directions relative to the snake's
    orientation and returns the normalized distance to the nearest
    obstacle (wall or own body) in that direction.

    Arguments:
        snake {Snake} -- The snake whose head the rays originate from.

    Returns:
        list of float -- 8 values in (0, 1], where 1.0 means the nearest
        obstacle is as far away as the grid allows and small values mean
        it is close.
    """
    head_x, head_y = snake.coords[0]
    body = set(snake.coords[1:])
    rays = []

    for dx, dy in _directions_for(snake.orientation):
        x, y = head_x, head_y
        steps = 0
        while True:
            x += dx
            y += dy
            steps += 1
            if x < 0 or x > GRID_SIZE - 1 or y < 0 or y > GRID_SIZE - 1:
                break
            if (x, y) in body:
                break
            if steps >= MAX_STEPS:
                break
        rays.append(min(steps, MAX_STEPS) / MAX_STEPS)

    return rays


def cast_food_rays(snake, food):
    """
    Casts a ray in each of the 8 directions relative to the snake's
    orientation and returns the normalized distance to the food if it lies
    exactly on that ray, or 0.0 otherwise.

    Arguments:
        snake {Snake} -- The snake whose head the rays originate from.
        food {Food} -- The food to detect.

    Returns:
        list of float -- 8 values in [0, 1). Closer food gives a higher
        value; a direction not aligned with the food gives 0.0.
    """
    head_x, head_y = snake.coords[0]
    dx_f, dy_f = food.x - head_x, food.y - head_y
    rays = []

    for dx, dy in _directions_for(snake.orientation):
        aligned, steps = _alignment(dx, dy, dx_f, dy_f)
        rays.append(1 - steps / MAX_STEPS if aligned else 0.0)

    return rays


def _alignment(dx, dy, dx_f, dy_f):
    """
    Determines whether the food offset (dx_f, dy_f) lies on the ray cast in
    direction (dx, dy), and if so, how many steps away it is.
    """
    if dx == 0:
        if dx_f != 0 or dy_f == 0 or (dy_f > 0) != (dy > 0):
            return False, 0
        return True, abs(dy_f)
    if dy == 0:
        if dy_f != 0 or dx_f == 0 or (dx_f > 0) != (dx > 0):
            return False, 0
        return True, abs(dx_f)

    if dx_f == 0 or dy_f == 0 or abs(dx_f) != abs(dy_f):
        return False, 0
    if (dx_f > 0) != (dx > 0) or (dy_f > 0) != (dy > 0):
        return False, 0
    return True, abs(dx_f)
