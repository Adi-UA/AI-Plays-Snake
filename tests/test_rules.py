from gamesrc.rules import has_failed, hit_self, hit_wall
from gamesrc.snake import Snake


def test_hit_self_true_when_head_matches_a_body_segment():
    snake = Snake()
    snake.coords = [(5, 5), (6, 5), (5, 5)]
    assert hit_self(snake)


def test_hit_self_false_for_a_healthy_snake():
    assert not hit_self(Snake())


def test_hit_wall_true_when_head_leaves_the_grid():
    snake = Snake()
    snake.coords = [(-1, 5)] + snake.coords[1:]
    assert hit_wall(snake)


def test_hit_wall_false_inside_the_grid():
    assert not hit_wall(Snake())


def test_has_failed_is_the_union_of_both_conditions():
    snake = Snake()
    assert not has_failed(snake)

    snake.coords = [(-1, 5)] + snake.coords[1:]
    assert has_failed(snake)
