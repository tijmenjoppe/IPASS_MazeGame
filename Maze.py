import numpy as np
import random


class Maze:
    def __init__(self, x, y, gen_func = None):
        """
        creates empty maze of size (y^2 + 1) * (x^2 +1)
        y, x representing the number of nodes that will be placed on uneven rows/cols (0-visited 1-not-visited).
        Even rows/cols will represent edges/walls (1).
        The maze starts out as a grid filled with Ones and the passages will be carved out
        :param y: number of nodes on y axis
        :param x: number of nodes on x axis
        """
        gen_funcs = {'DFS': self.__depth_first_search}
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
        """"function to get list of neighbors relative to a given xpos, ypos
        we only look for neighbors from and on the uneven x / y axis this is because all the even rows/cols are walls/edges

        params:
            x: x position
            y: y position
            shuffle: True or False to shuffle the list of neighbors before return
        returns:
            list of neighbor relative to (x, y) position
            """
        # list comprehension to return neighbors. Only returns neighbors existent in the graph.
        # ex: cell 1, 1 only has 2 neighbors
        n = [*[(xpos + i, ypos) for i in range(-2, 3, 4) if 0 <= xpos + i <= self.rows - 1],
             *[(xpos, ypos + i) for i in range(-2, 3, 4) if 0 <= ypos + i <= self.cols - 1]]
        if shuffle:
            random.shuffle(n)
        return n

    # generators will eventually be used as private methods used once at init
    def __depth_first_search(self, start=(1, 1)):
        # backtracking stack
        stack = [start]
        # default starting cell is first (uneven!) cell in the graph
        self.graph[start] = 0
        while stack:
            # current cell
            current_x, current_y = stack[-1]
            # find neighbors and filter out the already visited neighbors (value on graph is 0)
            neighbors = [n for n in self.neighbors(current_x, current_y, True) if self.graph[n] == 1]
            if len(neighbors) == 0:
                stack = stack[:-1]
            else:
                # make neighbor a open cell (0)
                next_x, next_y = neighbors[0]
                self.graph[next_x, next_y] = 0
                # make wall between neighbor and current cell open (0)
                self.graph[(current_x + next_x) // 2][(current_y + next_y) // 2] = 0
                stack.append((next_x, next_y))


m = Maze(3, 3, 'DFS')
m2 = Maze(3, 6, 'DFS')
m3 = Maze(6, 3, 'DFS')
m4 = Maze(30, 30, 'DFS')

print(m.graph)
print(m2.graph)
print(m3.graph)
print(m4.graph)
