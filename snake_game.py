import pygame

from gamesrc.decision import generate_food
from gamesrc.grid import Grid
from gamesrc.render import draw, init_display
from gamesrc.rules import has_failed
from gamesrc.snake import Snake

FPS = 17


def main():
    """This function runs the game for a human player using the arrow keys."""
    display = init_display()

    grid = Grid()
    snake = Snake()
    food = generate_food(grid, snake)
    score = 0

    running = True
    while running:
        display.tick(FPS)

        move = None
        for event in display.poll_events():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    move = "L"
                elif event.key == pygame.K_RIGHT:
                    move = "R"

        if move is None:
            snake.tick(grid)
        else:
            snake.move(grid, move)

        if snake.collide(food):
            score += 1
            snake.elongate(grid)
            display.on_food_eaten()
            food = generate_food(grid, snake)

        if has_failed(snake):
            running = False
            break

        draw(display, snake, food, score)


if __name__ == "__main__":
    main()
