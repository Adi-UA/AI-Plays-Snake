import pygame
import numpy
import random
import neat
import os
import pickle
from resources.reference import *
from resources.util import *
from gamesrc.grid import Grid
from gamesrc.snake import Snake
from gamesrc.food import Food


def has_failed(snake, genome):
    """
    This function checks to see if the snake has met any of the fail conditions.
    Since the grid is a standard 30 by 30 grid, the grid object is not required
    to check extremes.

    Arguments:
        snake {Snake} -- The snake whose status is to be found.
        genome -- The genome controlling this snake

    Returns:
        boolean -- true if it has met a fail condition and False otherwise.
    """
    x, y = snake.coords[0][0], snake.coords[0][1]
    if ((x, y) in snake.coords[1:]):
        genome.fitness -= 3  # Loses a lot of points for hitting itself
        return True
    elif x < 0 or x > 29 or y < 0 or y > 29:
        # Loses slightly less pints for hitting the wall because inputs used for
        # the NN generally mean this case is already rare.

        genome.fitness -= 2.5
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


def eval(genomes, config):
    """
    This function runs the game and evalutes the NNs formed from the given config.
    """

    global FOOD_RGB

    for _, genome in genomes:

        network = neat.nn.FeedForwardNetwork.create(genome, config)
        genome.fitness = 0

        grid = Grid()
        snake = Snake()
        food = generate_food(grid, snake)
        score = 0

        # Used to track time since distance from current food and time since
        # last food
        food_cur_dist = (abs(food.x -
                             snake.coords[0][0]), abs(food.y -
                                                      snake.coords[0][1]))
        last_food = pygame.time.get_ticks()

        isRunning = True
        while isRunning:
            game_clock.tick(1000)  # I am speed

            # Time since last food in seconds
            time_since_food = (pygame.time.get_ticks() - last_food) / 1000

            # At 1000fps if it hasn't found food in 4 seconds it is definitely
            # self looping so we stop it.
            if time_since_food >= 4:
                genome.fitness -= 500
                isRunning = False
                break

            # Handle Quitting
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    isRunning = False
                    pygame.quit()
                    quit()

            # Make a decision and use it
            decision = make_decision(network, grid, snake, food)
            max_val = max(decision)

            # Decision size is 3 and each index from 0 to 2 represents L,R and
            # nothing. We simply choose the maximum of these three to make a
            # decision.
            if max_val == decision[0]:
                snake.move(grid, "L")
            elif max_val == decision[1]:
                snake.move(grid, "R")
            else:
                snake.tick(grid)

            # Update current distance to food
            food_prev_dist = food_cur_dist
            food_cur_dist = (
                abs(food.x - snake.coords[0][0]), abs(food.y - snake.coords[0][1]))

            # If it moved closer to the food give it points and if it moved away
            # take away more points. On the whole self loops lose points
            if food_cur_dist[0] < food_prev_dist[0] or food_cur_dist[1] < food_prev_dist[1]:
                genome.fitness += 1
            else:
                genome.fitness -= 1.5

            # Check collision
            if snake.collide(food):
                last_food = pygame.time.get_ticks()  # Reset last food timer
                genome.fitness += 4  # Lots of fitness
                score += 1
                snake.elongate(grid)

                # RGB snakes are essential for training /s
                SNAKE_IMG.fill(FOOD_RGB)

                food = generate_food(grid, snake)

            # Check for failure and deduct points accordingly
            if has_failed(snake, genome):
                isRunning = False
                break

            draw(WINDOW, snake, food, score)

            # A score of 45 generally means it has gotten as good as it could
            # have, so we store the model
            if score >= 45:
                best_model = network
                nn_file = open("best_model.pickle", "wb")
                pickle.dump(best_model, nn_file)
                nn_file.close()

                isRunning = False
                break


def run(config_path):
    """
    This function runs each generation of NNs using the configuration file
    passed to it.

    Arguments:
        config_path  -- Path to the NNs config file
    """
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_path)

    population = neat.Population(config)
    population.add_reporter(neat.StdOutReporter(True))

    stats = neat.StatisticsReporter()
    population.add_reporter(stats)

    winner = population.run(eval, 50)


def main():
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, r"resources\config-feedforward.txt")
    run(config_path)


if __name__ == "__main__":
    main()
