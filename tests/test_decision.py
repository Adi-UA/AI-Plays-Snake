import pytest

from gamesrc.decision import build_inputs, generate_food, make_food_decision
from gamesrc.food import Food
from gamesrc.snake import Snake


def test_generate_food_never_lands_on_the_snake(grid, snake):
    for _ in range(50):
        food = generate_food(grid, snake)
        assert (food.x, food.y) not in snake.coords


def test_make_food_decision_picks_exactly_one_direction(grid):
    snake = Snake()
    food = Food(grid, snake.coords[0][0] + 5, snake.coords[0][1])
    decision = make_food_decision(snake, food)
    assert sum(decision) == 1


def test_build_inputs_legacy_has_eleven_values(grid, snake, food):
    assert len(build_inputs(grid, snake, food, "legacy")) == 11


def test_build_inputs_raycast_has_sixteen_values(grid, snake, food):
    assert len(build_inputs(grid, snake, food, "raycast")) == 16


def test_build_inputs_rejects_an_unknown_mode(grid, snake, food):
    with pytest.raises(ValueError):
        build_inputs(grid, snake, food, "bogus")
