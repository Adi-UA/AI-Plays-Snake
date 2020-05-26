import pygame

# Contains the global variables that are common in various parts of the program

pygame.init()
game_clock = pygame.time.Clock()

WIN_WIDTH = 450
WIN_HEIGHT = 450
WINDOW = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

ANIMATION_TICK = 25  # used to switch food colors

SNAKE_IMG = pygame.Surface((15, 15))
SNAKE_IMG.fill((0, 255, 0))

FOOD_RGB = (255, 0, 0)
FOOD_IMG = pygame.Surface((15, 15))
FOOD_IMG.fill((FOOD_RGB))

STAT_FONT = pygame.font.SysFont("comicsans", 50)
