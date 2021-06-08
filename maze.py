import numpy as np
import random
import maze_generators
import maze_solver


class Maze:
    def __init__(self, x, y, gen_func=None):
        """
        creates empty maze of size (y*2 + 1) * (x*2 +1)
        y, x representing the number of nodes that will be placed on uneven rows/cols (0-visited 1-not-visited).
        Even rows/cols will represent edges/walls (1).
        The maze starts out as a grid filled with Ones and the passages will be carved out
        :param y: number of nodes on y axis
        :param x: number of nodes on x axis
        """
        gen_funcs = {'DFS': maze_generators.depth_first_search, 'AB': maze_generators.aldous_broder,
                     'PRIM': maze_generators.prim}
        # len nodes x and y axis
        self.x = x
        self.y = y
        # len of whole graph including the nodes and their edges
        self.rows = 2 * y + 1
        self.cols = 2 * x + 1
        self.grid = np.ones((self.rows, self.cols)).astype(int)
        # start is at left up corner finish at right down
        self.start = (1, 1)
        self.end = (self.rows - 2, self.cols - 2)
        if gen_func:
            gen_funcs[gen_func](self)
        # maze represented as adj list
        self.adj_lst = {
            (i, j):
                [n for n in self.neighbors(i, j, radius=1)
                 if self.grid[n] == 0] for i in range(self.rows) for j in range(self.cols) if self.grid[i, j] == 0}
        self.solution = maze_solver.breadth_first_search(self.adj_lst, self.start, self.end)

    def neighbors(self, xpos, ypos, shuffle=True, radius=2):
        # list comprehension to return neighbors. Only returns neighbors existent in the graph.
        # ex: cell 1, 1 only has 2 neighbors
        # radius 2 to get neighbors from cell to cell (cells only on uneven cells)
        # radius 1 to get all neighbors (used to get graph of whole maze)
        n = [*[(xpos + i, ypos) for i in range(-radius, radius+1, radius*2) if 0 < xpos + i < self.rows - 1],  # and 0 < ypos <= self.cols
             *[(xpos, ypos + i) for i in range(-radius, radius+1, radius*2) if 0 < ypos + i < self.cols - 1]]  # and 0 < xpos <= self.rows
        if shuffle:
            random.shuffle(n)
        return n

    def destroy_wall(self, current_cell, neighbor_cell):
        """destroys a wall cell between 2 given cells"""
        self.grid[(current_cell[0] + neighbor_cell[0]) // 2][(current_cell[1] + neighbor_cell[1]) // 2] = 0
