import pygame
import random
import neat
import os
from resources.reference import *
from resources.util import *
from gamesrc.grid import Grid
from gamesrc.snake import Snake
from gamesrc.food import Food


def has_failed(snake):
    """
    This function checks to see if the snake has met any of the fail conditions.
    Since the grid is a standard 30 by 30 grid, the grid object is not required
    to check extremes.

    Arguments:
        snake {Snake} -- The snake whose status is to be found.

    Returns:
        boolean -- true if it has met a fail condition and False otherwise.
    """
    x, y = snake.coords[0][0], snake.coords[0][1]

    # Did it hit its own body?
    if ((x, y) in snake.coords[1:]):
        return True
    elif x < 0 or x > 29 or y < 0 or y > 29:  # Did it go outside the grid?
        return True
    else:
        return False


def draw(window, snake, food, score):
    """
    This function draws and updates the pygame window with the given information.

    Arguments:
        window {Surface} -- The active PyGame window
        snake {Snake} -- The snake in the game
        food {Food} -- The food in the game
        score {int} -- The current score
    """

    global ANIMATION_TICK
    ANIMATION_TICK -= 1  # Used to change food color

    window.fill((0, 0, 51))

    # Food color changing and drawing is handled here
    if ANIMATION_TICK == 0:
        global FOOD_RGB
        FOOD_RGB = (
            random.randrange(
                50, 255), random.randrange(
                50, 255), random.randrange(
                50, 255))
        FOOD_IMG.fill(FOOD_RGB)
        ANIMATION_TICK = 25
    else:
        window.blit(FOOD_IMG, (food.x * 15, food.y * 15))

    # Draw snake
    for i, coord in enumerate(snake.coords):
        x = coord[0] * 15
        y = coord[1] * 15

        if i == 0:
            head = pygame.Surface((15, 15))
            head.fill((255, 255, 255))
            WINDOW.blit(head, (x, y))
        else:
            WINDOW.blit(SNAKE_IMG, (x, y))

    # Draw Score
    score_txt = STAT_FONT.render("Score: " + str(score), 1, (255, 255, 255))
    window.blit(
        score_txt,
        (WIN_WIDTH - 10 - score_txt.get_width(), 10))  # top right of screen

    pygame.display.update()


def main():
    """This function runs the game for humans.
    """

    global FOOD_RGB  # Food needs RGB too
    grid = Grid()
    snake = Snake()
    food = generate_food(grid, snake)
    score = 0

    isRunning = True
    while isRunning:
        game_clock.tick(17)

        move = None
        for event in pygame.event.get():
            # Handle Quittiing
            if event.type == pygame.QUIT:
                isRunning = False
                pygame.quit()
                quit()

            # Check for key presses
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    move = "L"
                elif event.key == pygame.K_RIGHT:
                    move = "R"

        # Moves ahead if you didn't choose a move
        if move is None:
            snake.tick(grid)
        else:
            snake.move(grid, move)

        # Check if snake collided with the food
        if snake.collide(food):
            score += 1
            snake.elongate(grid)

            # Fancy color changing for snake :)
            SNAKE_IMG.fill(FOOD_RGB)

            food = generate_food(grid, snake)

        # Stop running in case
        if has_failed(snake):
            isRunning = False
            break

        draw(WINDOW, snake, food, score)


if __name__ == "__main__":
    main()
