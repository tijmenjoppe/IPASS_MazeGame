"""Script to visualize implemented algorithms"""

from maze_game.maze_logic.maze import *
from maze_game.maze_logic.maze_solvers import depth_first_search, breadth_first_search
import time

for generator in gen_funcs:
    Maze(3,3,generator, 10)

maze = Maze(30,30, 3)
breadth_first_search(maze, maze.start, 60)
time.sleep(1)
depth_first_search(maze, maze.start, 60)
time.sleep(1)