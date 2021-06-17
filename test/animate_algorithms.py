"""Script to visualize implemented algorithms"""

from maze_game.maze.maze import *
from maze_game.maze.maze_solvers import depth_first_search, breadth_first_search
import time


for generator in gen_funcs:
    Maze(9,9,generator, 30)


maze = Maze(30,30, 3)
breadth_first_search(maze, maze.start, 60)
time.sleep(1)
depth_first_search(maze, maze.start, 60)
time.sleep(1)