import os
import random

# Importing pygame prints a support banner by default. Parallel training
# imports this module once per worker process, so that banner would print
# once per worker; suppress it here.
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")
import pygame

from gamesrc.constants import CELL_PX, WIN_HEIGHT, WIN_WIDTH

FOOD_COLOR_TICKS = 25  # ticks between food color changes


class Display:
    """
    Holds the pygame window, clock, and drawable surfaces for one game.
    Nothing here runs at import time; a Display is only created when a
    caller actually wants visuals.
    """

    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("comicsans", 50)

        self.food_rgb = (255, 0, 0)
        self.food_img = pygame.Surface((CELL_PX, CELL_PX))
        self.food_img.fill(self.food_rgb)

        self.snake_img = pygame.Surface((CELL_PX, CELL_PX))
        self.snake_img.fill((0, 255, 0))

        self.color_tick = FOOD_COLOR_TICKS

    def tick(self, fps):
        self.clock.tick(fps)

    def poll_events(self):
        return pygame.event.get()

    def on_food_eaten(self):
        """Recolors the snake to the food's current color."""
        self.snake_img.fill(self.food_rgb)


def init_display():
    """
    Initializes pygame and opens the game window. Call only when visuals
    are actually wanted (never at import time), since this is what makes
    headless, multi-process training possible.
    """
    return Display()


def draw(display, snake, food, score):
    """
    Draws one frame: background, food (color-cycling), snake, and score.

    Arguments:
        display {Display} -- The active display resources.
        snake {Snake} -- The snake to draw.
        food {Food} -- The food to draw.
        score {int} -- The current score.
    """
    window = display.window

    display.color_tick -= 1
    if display.color_tick == 0:
        display.food_rgb = (
            random.randrange(50, 255),
            random.randrange(50, 255),
            random.randrange(50, 255),
        )
        display.food_img.fill(display.food_rgb)
        display.color_tick = FOOD_COLOR_TICKS

    window.fill((0, 0, 51))
    window.blit(display.food_img, (food.x * CELL_PX, food.y * CELL_PX))

    for i, (x, y) in enumerate(snake.coords):
        px, py = x * CELL_PX, y * CELL_PX
        if i == 0:
            head = pygame.Surface((CELL_PX, CELL_PX))
            head.fill((255, 255, 255))
            window.blit(head, (px, py))
        else:
            window.blit(display.snake_img, (px, py))

    score_txt = display.font.render(f"Score: {score}", 1, (255, 255, 255))
    window.blit(score_txt, (WIN_WIDTH - 10 - score_txt.get_width(), 10))

    pygame.display.update()


def make_step_callback(display, fps):
    """
    Builds an `on_step` callback for `episode.run_episode` that renders
    each tick and quits cleanly on a window-close event. Used to watch a
    network-driven game play out (testAI.py, or `trainAI.py --render`).

    Arguments:
        display {Display} -- The active display resources.
        fps {int} -- Frame rate to cap the callback at.

    Returns:
        callable -- `on_step(grid, snake, food, score)`.
    """
    last_score = 0

    def on_step(grid, snake, food, score):
        nonlocal last_score

        for event in display.poll_events():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit

        if score > last_score:
            display.on_food_eaten()
        last_score = score

        draw(display, snake, food, score)
        display.tick(fps)

    return on_step
