from gamesrc.food import Food
from gamesrc.snake import Snake


def test_snake_spawns_facing_right_with_six_segments(grid):
    snake = Snake()
    assert snake.orientation == "R"
    assert len(snake.coords) == 6


def test_tick_moves_head_one_cell_without_changing_length(grid):
    snake = Snake()
    head = snake.coords[0]
    length_before = len(snake.coords)

    snake.tick(grid)

    assert snake.coords[0] == (head[0] + 1, head[1])
    assert len(snake.coords) == length_before


def test_move_left_then_right_returns_to_the_original_orientation(grid):
    snake = Snake()
    original = snake.orientation

    snake.move(grid, "L")
    turned = snake.orientation
    assert turned != original

    snake.move(grid, "R")
    assert snake.orientation == original


def test_elongate_adds_a_segment_ahead_of_the_old_head(grid):
    snake = Snake()
    before = list(snake.coords)

    snake.elongate(grid)

    assert len(snake.coords) == len(before) + 1
    assert snake.coords[1:] == before


def test_collide_true_only_when_head_is_on_the_food(grid):
    snake = Snake()
    head = snake.coords[0]

    assert snake.collide(Food(grid, head[0], head[1]))
    assert not snake.collide(Food(grid, head[0] + 5, head[1] + 5))


def test_get_8_adjacent_returns_eight_binary_values(grid):
    snake = Snake()
    adjacent = snake.get_8_adjacent(grid)
    assert len(adjacent) == 8
    assert all(v in (0, 1) for v in adjacent)
