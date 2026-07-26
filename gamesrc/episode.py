from gamesrc.decision import build_inputs, generate_food
from gamesrc.grid import Grid
from gamesrc.rules import hit_self, hit_wall
from gamesrc.snake import Snake

# A genome that hasn't eaten in this many ticks is treated as self-looping
# and cut off. Mirrors the original wall-clock "4 seconds at 1000fps" rule,
# expressed as a tick count so training has no pygame/timer dependency.
STARVATION_LIMIT = 4000

# A score this high means play is essentially solved; no need to keep going.
WIN_SCORE = 45


def run_episode(net, input_mode="legacy", on_step=None):
    """
    Plays one full episode of snake driven entirely by `net`, with no
    pygame dependency. This is the single game loop used by both headless
    training (safe to run inside a worker process) and rendering, via the
    optional `on_step` hook.

    Arguments:
        net -- A network exposing `.activate(inputs) -> list of float`.
        input_mode {str} -- "legacy" or "raycast", see `decision.build_inputs`.
        on_step -- Optional callback `on_step(grid, snake, food, score)`
        invoked once per tick, after the move and before the next decision.

    Returns:
        dict -- {"fitness": float, "score": int, "steps": int}
    """
    grid = Grid()
    snake = Snake()
    food = generate_food(grid, snake)

    fitness = 0.0
    score = 0
    steps = 0
    steps_since_food = 0
    food_dist = _distance(snake, food)

    while True:
        steps += 1
        steps_since_food += 1

        if steps_since_food >= STARVATION_LIMIT:
            fitness -= 500
            break

        decision = net.activate(build_inputs(grid, snake, food, input_mode))
        max_val = max(decision)

        if max_val == decision[0]:
            snake.move(grid, "L")
        elif max_val == decision[1]:
            snake.move(grid, "R")
        else:
            snake.tick(grid)

        # Reward getting closer on either axis, penalize otherwise. This is
        # a component-wise check (not total distance), matching the
        # original tuning.
        new_food_dist = _distance(snake, food)
        if new_food_dist[0] < food_dist[0] or new_food_dist[1] < food_dist[1]:
            fitness += 1
        else:
            fitness -= 1.5
        food_dist = new_food_dist

        if snake.collide(food):
            steps_since_food = 0
            fitness += 4
            score += 1
            snake.elongate(grid)
            food = generate_food(grid, snake)
            food_dist = _distance(snake, food)

        if hit_self(snake):
            fitness -= 3
            break
        if hit_wall(snake):
            fitness -= 2.5
            break

        if on_step is not None:
            on_step(grid, snake, food, score)

        if score >= WIN_SCORE:
            break

    return {"fitness": fitness, "score": score, "steps": steps}


def _distance(snake, food):
    head_x, head_y = snake.coords[0]
    return abs(food.x - head_x), abs(food.y - head_y)
