import unittest
from maze_game.maze import Maze
from maze_game.maze.maze_solvers import *
import numpy as np


# test class to test the solving/pathfinding algorithms
class TestMazeSolvers(unittest.TestCase):
    # Depth first search
    def test_DFS(self):
        maze = Maze(3, 3)
        maze.grid = np.array([[1, 1, 1, 1, 1, 1, 1],
                              [1, 0, 1, 0, 0, 0, 1],
                              [1, 0, 1, 0, 0, 0, 1],
                              [1, 0, 1, 0, 0, 0, 1],
                              [1, 0, 1, 1, 1, 1, 1],
                              [1, 0, 0, 0, 0, 0, 1],
                              [1, 1, 1, 1, 1, 1, 1]])
        path = depth_first_search(maze, (1, 1))
        self.assertEqual(len(path), 9)

    def test_BFS(self):
        maze = Maze(3, 3)
        maze.grid = np.array([[1, 1, 1, 1, 1, 1, 1],
                              [1, 0, 0, 0, 0, 0, 1],
                              [1, 0, 0, 0, 0, 0, 1],
                              [1, 0, 0, 0, 0, 0, 1],
                              [1, 0, 0, 0, 0, 0, 1],
                              [1, 0, 0, 0, 0, 0, 1],
                              [1, 1, 1, 1, 1, 1, 1]])
        path = breadth_first_search(maze, (1, 1))
        # shortest path can be multiple paths but always of length 9
        self.assertEqual(len(path), 9)
        maze.grid = np.array([[1, 1, 1, 1, 1, 1, 1],
                              [1, 0, 1, 0, 0, 0, 1],
                              [1, 0, 1, 0, 0, 0, 1],
                              [1, 0, 1, 0, 0, 0, 1],
                              [1, 0, 1, 0, 1, 0, 1],
                              [1, 0, 0, 0, 0, 0, 1],
                              [1, 1, 1, 1, 1, 1, 1]])
        path = breadth_first_search(maze, (1, 1))
        # shortest path will always be:
        self.assertEqual(path, [(1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (5, 2), (5, 3), (5, 4), (5, 5)])



if __name__ == '__main__':
    unittest.main()
