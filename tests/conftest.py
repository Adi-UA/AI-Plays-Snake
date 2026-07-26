import pytest

from gamesrc.decision import generate_food
from gamesrc.grid import Grid
from gamesrc.snake import Snake


@pytest.fixture
def grid():
    return Grid()


@pytest.fixture
def snake():
    return Snake()


@pytest.fixture
def food(grid, snake):
    return generate_food(grid, snake)
