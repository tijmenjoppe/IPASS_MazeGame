"""contains functions used by both solvers and generators to animate the solving/generator algorithm"""
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)


def animation_setup_grid(grid, tile_size=15):
    pygame.init()
    clock = pygame.time.Clock()
    tile_size = tile_size
    win = pygame.display.set_mode((len(grid)*tile_size, len(grid[0])*tile_size))
    return clock, tile_size, win

def draw_grid(win,grid, tile_size, wall_color=BLACK, path_color=WHITE):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    cols = len(grid[0])
    rows = len(grid)
    win.fill(path_color)
    for Y in range(cols):
        for X in range(rows):
            x = X * tile_size
            y = Y * tile_size
            if grid[X][Y] == 1:
                pygame.draw.rect(win, wall_color, (x, y, tile_size, tile_size))