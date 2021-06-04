import numpy as np
import random
import maze_generators

class Maze:
    def __init__(self, x, y, gen_func=None):
        """
        creates empty maze of size (y^2 + 1) * (x^2 +1)
        y, x representing the number of nodes that will be placed on uneven rows/cols (0-visited 1-not-visited).
        Even rows/cols will represent edges/walls (1).
        The maze starts out as a grid filled with Ones and the passages will be carved out
        :param y: number of nodes on y axis
        :param x: number of nodes on x axis
        """
        gen_funcs = {'DFS': maze_generators.depth_first_search, 'AB': maze_generators.aldous_broder}
        # len nodes x and y axis
        self.x = x
        self.y = y
        # len of whole graph including the nodes and their edges
        self.rows = 2 * y + 1
        self.cols = 2 * x + 1
        self.graph = np.ones((self.rows, self.cols)).astype(int)
        # start is at left up corner finish at right down
        self.start = (1, 1)
        self.end = (self.rows-2, self.cols-2)
        gen_funcs[gen_func](self)

    def neighbors(self, xpos, ypos, shuffle=True):
        # list comprehension to return neighbors. Only returns neighbors existent in the graph.
        # ex: cell 1, 1 only has 2 neighbors
        n = [*[(xpos + i, ypos) for i in range(-2, 3, 4) if 0 <= xpos + i <= self.rows - 1],
             *[(xpos, ypos + i) for i in range(-2, 3, 4) if 0 <= ypos + i <= self.cols - 1]]
        if shuffle:
            random.shuffle(n)
        return n

    def destroy_wall(self, current_cell, neighbor_cell):
        """destroys a wallcell between 2 given cells"""
        self.graph[(current_cell[0] + neighbor_cell[0]) // 2][(current_cell[1] + neighbor_cell[1]) // 2] = 0


m = Maze(3, 3, 'DFS')
print(m.graph)
print(m.end)

print(m.graph)

