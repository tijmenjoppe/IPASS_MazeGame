import numpy as np
import random
class Maze:
    def __init__(self, y, x):
        """
        creates empty maze of size (y^2 + 1) * (x^2 +1)
        y, x representing the number of nodes that will be placed on uneven rows/cols (0-visited 1-not-visited).
        Even rows/cols will represent edges/walls (1)
        :param y: number of nodes on y axis
        :param x: number of nodes on x axis
        """
        self.rows = 2 * x + 1
        self.cols = 2 * y + 1
        self.graph = np.zeros((self.rows, self.cols))
        #for i in range(0, self.rows, 2):
        #    self.graph[i, :] = 1
        #for i in range(0, self.rows, 2):
        #    self.graph[:, i] = 1

    def neighbors(self, xpos, ypos):
        """"function to get list of neighbors relative to a given xpos, ypos
        we only look for neighbors from and on the uneven x / y axis this is because all the even rows/cols are walls/edges

        params:
            x: x position
            y: y position
        returns:
            list of neighbor (x, y) positions
            """

        # list comprehension to return neighbors. Only returns neighbors existent in the graph.
        # ex: cell 1, 1 only has 2 neighbors
        return [(xpos + i, ypos) for i in range(-2, 3, 4) if 0 <= xpos + i <= self.rows - 1 and self.graph[xpos+i][ypos]] + \
               [(xpos, ypos + i) for i in range(-2, 3, 4) if 0 <= ypos + i <= self.cols - 1 and self.graph[xpos][ypos+i]]

