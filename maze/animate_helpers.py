"""contains functions used by both solvers and generators to animate the solving/generator algorithm"""
import pygame
from rgb_colors import *

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