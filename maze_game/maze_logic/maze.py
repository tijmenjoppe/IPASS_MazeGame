"""Module to create a maze object"""

import numpy as np
from functools import partial

from maze_game.maze_logic.maze_generators import *

# Easy: Depth First Search. Medium: Prim. Hard: Wilson & Aldous Broder hybrid (extension on Wilson)
gen_funcs = {1: depth_first_search,
             2: prim, 3: partial(wilson, extra_walker=True), 4: wilson, 5: aldous_broder}


class Maze:
    """ Maze object which stores a perfect maze in form of a grid & adjacent list
    Attributes:
        x (int): length of number of cells in cols
        y (int): length of number of cells in rows
        rows (int): total length of rows (cells & walls combined) == nr of cells in row (x) * 2 + 1.
        cols (int): total length of cols
        grid (2d numpy array): maze represented as grid starting as a full grid of 1's so the maze can be carved out.
        start (tuple): position in the grid which is the starting position of the maze. always left upper corner
        end (tuple): position in the grid which is the end/finish position of the maze. always right lower corner
    """

    def __init__(self, x, y, gen_func=None, animate=False):
        """
        creates empty maze of size (y*2 + 1) * (x*2 +1)
        y, x representing the number of nodes/cells that will be placed on uneven rows/cols (0-visited 1-not-visited).
        Even rows/cols will represent closed edges/walls as (1) and actual edges/opened edges as (0).
        The maze starts out as a grid filled with Ones and the passages will be carved out
        Args:
            x (int): number of cells(vertices) on x axis
            y (int): number of cells(vertices) on y axis
            gen_func: which generation algorithm to use
        animate: animate the generating process, 0 (=False) or FPS as integer value.

        """
        # len nodes x and y axis
        self.x = x
        self.y = y
        # nodes including their possible edges (walls)
        self.rows = 2 * y + 1
        self.cols = 2 * x + 1
        # make a grid for example  for x = 3 y = 3 a 7x7 2d array with 1's
        self.grid = np.ones((self.rows, self.cols)).astype(int)
        # start is at left up corner finish at right down
        self.start = (1, 1)
        self.end = (self.rows - 2, self.cols - 2)
        # carve out a maze with a given generation algorithm/function
        if gen_func:
            gen_funcs[gen_func](self, animate=animate)

    @property
    def adj_lst(self):
        """Generates a adjacent list from a maze in grid form
        Returns:
            maze represented as adjacent list
         """
        return {
            (i, j):
                [n for n in self.neighbors(i, j, radius=1)
                 if self.grid[n] == 0] for i in range(self.rows) for j in range(self.cols) if self.grid[i, j] == 0}

    def destroy_wall(self, current_cell, neighbor_cell):
        """function to destroy a wall between 2 given cells
        Args:
            current_cell(tuple): cell position (row, col)
            neighbor_cell(tuple): neighboring cell position (row, col) """
        self.grid[(current_cell[0] + neighbor_cell[0]) // 2][(current_cell[1] + neighbor_cell[1]) // 2] = 0

    def neighbors(self, row_pos, col_pos, shuffle=True, radius=2):
        """ function to get the neighbors of a certain position in the grid.
        ex: cell 1, 1 only has 2 neighbors (if radius == 2)
        radius 2 to get neighbors from cell to cell (cells only on uneven cells)
        radius 1 to get all neighbors (used to create adj list representation of maze)
        Args:
            row_pos : row position of target cell to find neighbors
            col_pos : col position of target cell to find neigbbors
            shuffle : Boolean whether to shuffle the result
            radius : At what radius to look for neighbors?
        Returns:
            list of neighbors"""
        # get neighbors in radius on x axis and y axis add these 2 together to get all neighbors
        neighbors_lst = [*[(row_pos + i, col_pos) for i in range(-radius, radius + 1, radius * 2) if
               0 < row_pos + i < self.rows - 1],
             *[(row_pos, col_pos + i) for i in range(-radius, radius + 1, radius * 2) if
               0 < col_pos + i < self.cols - 1]]
        if shuffle:
            random.shuffle(neighbors_lst)
        return neighbors_lst
