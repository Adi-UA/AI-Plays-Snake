from gamesrc.food import Food
from gamesrc.sensors import MAX_STEPS, cast_food_rays, cast_obstacle_rays
from gamesrc.snake import Snake


def test_front_obstacle_ray_hits_the_wall(grid):
    snake = Snake()
    snake.orientation = "U"
    snake.coords = [(15, 3)]

    rays = cast_obstacle_rays(snake)

    assert rays[0] == 4 / MAX_STEPS  # blocked one cell past the y=0 wall


def test_front_obstacle_ray_stops_at_own_body_before_the_wall(grid):
    snake = Snake()
    snake.orientation = "U"
    snake.coords = [(15, 10), (15, 8)]  # body two cells ahead of the head

    rays = cast_obstacle_rays(snake)

    assert rays[0] == 2 / MAX_STEPS


def test_food_ray_is_zero_when_not_aligned_with_any_direction(grid):
    snake = Snake()
    snake.orientation = "U"
    snake.coords = [(15, 15)]
    food = Food(grid, 20, 22)  # neither axis- nor diagonal-aligned

    assert all(r == 0.0 for r in cast_food_rays(snake, food))


def test_food_ray_detects_food_straight_ahead(grid):
    snake = Snake()
    snake.orientation = "U"
    snake.coords = [(15, 15)]
    food = Food(grid, 15, 10)  # 5 cells straight up

    rays = cast_food_rays(snake, food)

    assert rays[0] == 1 - 5 / MAX_STEPS
    assert all(r == 0.0 for i, r in enumerate(rays) if i != 0)


def test_food_ray_detects_food_on_a_diagonal(grid):
    snake = Snake()
    snake.orientation = "U"
    snake.coords = [(15, 15)]
    food = Food(grid, 18, 12)  # 3 cells up and 3 cells right

    rays = cast_food_rays(snake, food)

    assert rays[1] == 1 - 3 / MAX_STEPS  # front-right diagonal
