import numpy as np
import random


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
        gen_funcs = {'DFS': self.__depth_first_search, 'AB': self.__aldous_broder}
        # len nodes x and y axis
        self.x = x
        self.y = y
        # len of whole graph including the nodes and their edges
        self.rows = 2 * y + 1
        self.cols = 2 * x + 1
        self.graph = np.ones((self.rows, self.cols)).astype(int)
        if gen_func:
            gen_funcs[gen_func]()

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

    def __depth_first_search(self, start=(1, 1)):
        # backtracking stack
        stack = [start]
        # default starting cell is first (uneven!) cell in the graph
        self.graph[start] = 0
        while stack:
            # current cell
            current_cell = stack[-1]
            # find neighbors and filter out the already visited neighbors (value on graph is 0)
            neighbors = [n for n in self.neighbors(current_cell[0], current_cell[1], True) if self.graph[n] == 1]
            if len(neighbors) == 0:
                stack = stack[:-1]
            else:
                # make neighbor a open cell (0)
                next_cell = neighbors[0]
                self.graph[next_cell] = 0
                # destroy wall between neighbor and current cell
                self.destroy_wall(current_cell, next_cell)
                stack.append(next_cell)

    def __aldous_broder(self, start=(1, 1)):
        visited_cells = [start]
        current_cell = start
        while len(visited_cells) < (self.x * self.y):
            self.graph[current_cell] = 0
            neighbors = self.neighbors(current_cell[0], current_cell[1], True)
            print(neighbors)
            next_cell = neighbors[0]
            if self.graph[next_cell]:
                visited_cells.append(next_cell)
                self.destroy_wall(current_cell, next_cell)
                self.graph[next_cell] = 0
            current_cell = next_cell


m = Maze(3, 3, 'AB')
print(m.graph)
