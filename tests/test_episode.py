from gamesrc import episode
from gamesrc.food import Food

_STEP_BY_ORIENTATION = {"U": (0, -1), "D": (0, 1), "L": (-1, 0), "R": (1, 0)}


class ForwardNet:
    """A stub network that always chooses to go forward."""

    def activate(self, inputs):
        return [0, 0, 1]


def test_forward_only_net_eventually_hits_the_wall():
    result = episode.run_episode(ForwardNet(), input_mode="legacy")
    assert result["steps"] < episode.STARVATION_LIMIT
    assert result["fitness"] != 0


def test_run_episode_works_with_raycast_mode():
    result = episode.run_episode(ForwardNet(), input_mode="raycast")
    assert result["steps"] > 0


def test_starvation_ends_the_episode_with_a_penalty(monkeypatch):
    monkeypatch.setattr(episode, "STARVATION_LIMIT", 3)
    monkeypatch.setattr(episode, "generate_food", lambda grid, snake: Food(grid, 0, 0))

    result = episode.run_episode(ForwardNet(), input_mode="legacy")

    assert result["steps"] == 3
    assert result["score"] == 0
    assert result["fitness"] < 0


def test_reaching_win_score_ends_the_episode(monkeypatch):
    def food_one_step_ahead(grid, snake):
        head_x, head_y = snake.coords[0]
        dx, dy = _STEP_BY_ORIENTATION[snake.orientation]
        return Food(grid, head_x + dx, head_y + dy)

    monkeypatch.setattr(episode, "generate_food", food_one_step_ahead)
    monkeypatch.setattr(episode, "WIN_SCORE", 1)

    result = episode.run_episode(ForwardNet(), input_mode="legacy")

    assert result["score"] == 1
    assert result["steps"] == 1
    assert result["fitness"] > 0
