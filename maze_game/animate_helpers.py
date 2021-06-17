"""contains functions used by both solvers and generators to animate the solving/generator algorithms
    and also color constants for all pygame instances"""
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"  # remove pygame welcome msg
import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0,153,0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
INDIGO = (75, 0, 130)


def animation_setup_grid(grid, tile_size=15):
    """Function to setup a pygame screen for animating solver/generator algorithms
    args:
        grid (2d array): maze as grid used to set display dimensions according to it's size
        tile_size (int): size of tiles in animation
    returns:
       clock(to manage fps) tile_size(to draw cells the appropriate size) win (pygame window) """
    pygame.init()
    clock = pygame.time.Clock()
    tile_size = tile_size
    cols = len(grid[0])
    rows = len(grid)
    win = pygame.display.set_mode((cols * tile_size, rows * tile_size))
    return clock, tile_size, win


def draw_grid(win, grid, tile_size, wall_color=BLACK, path_color=WHITE):
    """Function to draw a grid containing 1's and 0's on a given pygame display
    args:
        win (pygame surface): pygame display
        grid (2d array): maze as grid containing 1's for walls/no edge and 0's for open cells
        tile_size (int): size of tiles in animation
        wall_color (tuple): rgb color to display walls
        path_color: rgb color to display open cells"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    cols = len(grid[0])
    rows = len(grid)

    for r in range(rows):
        for c in range(cols):
            x = c * tile_size
            y = r * tile_size
            if grid[r][c] == 1:
                pygame.draw.rect(win, wall_color, (x, y, tile_size, tile_size))
            elif grid[r][c] == 0:
                pygame.draw.rect(win, path_color, (x, y, tile_size, tile_size))


def draw_start_finish(win, tile_size, start, end):
    """function to draw the start and end position a maze (used for visualizing solvers)
    args:
        win(pygame surface): pygame display
        tile_size(int): size of tiles in animation
        start(tuple): start position of the maze as (row, col)
        end(tuple): end/finish position of the maze as (row, col)"""
    pygame.draw.rect(win, RED, (start[1] * tile_size, start[0] * tile_size, tile_size, tile_size))
    pygame.draw.rect(win, YELLOW, (end[1] * tile_size, end[0] * tile_size, tile_size, tile_size))
