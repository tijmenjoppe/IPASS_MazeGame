import unittest
from maze_game.maze_logic.maze import Maze
import random
import numpy as np


class TestMaze(unittest.TestCase):
    def test_size(self):
        # maze of size  n1 * n2. n = random number
        height = random.randint(0, 100)
        width = random.randint(0, 100)

        maze = Maze(width, height)
        self.assertEqual(maze.y, height)
        self.assertEqual(maze.x, width)

        self.assertEqual(maze.rows, height * 2 + 1)
        self.assertEqual(maze.cols, width * 2 + 1)

    # test if adj list gets created and adjusted properly
    def test_adj_list(self):
        # maze full with 1's ( no edges ) so adj list representation should be empty
        maze = Maze(3, 3)
        self.assertEqual(len(maze.adj_lst), 0)

        maze.grid = np.array([[1, 1, 1, 1, 1, 1, 1],
                              [1, 0, 1, 0, 1, 0, 1],
                              [1, 1, 1, 1, 1, 1, 1],
                              [1, 0, 1, 0, 1, 0, 1],
                              [1, 1, 1, 1, 1, 1, 1],
                              [1, 0, 1, 0, 1, 0, 1],
                              [1, 1, 1, 1, 1, 1, 1]])
        self.assertEqual(maze.adj_lst,
                         {(1, 1): [], (1, 3): [], (1, 5): [], (3, 1): [], (3, 3): [], (3, 5): [], (5, 1): [],
                          (5, 3): [], (5, 5): []})


        maze.grid = np.array([[1, 1, 1, 1, 1, 1, 1],
                              [1, 0, 0, 1, 1, 1, 1],
                              [1, 0, 1, 1, 1, 1, 1],
                              [1, 1, 1, 1, 1, 1, 1],
                              [1, 1, 1, 1, 1, 1, 1],
                              [1, 1, 1, 1, 1, 1, 1],
                              [1, 1, 1, 1, 1, 1, 1]])
        # (1,1) is connected to (1,2) and (2,1)
        # (1,2) and (2,1) are only connected to (1,1)
        self.assertEqual(maze.adj_lst, {(1, 1): [(2, 1), (1, 2)], (1, 2): [(1, 1)], (2, 1): [(1, 1)]})

if __name__ == '__main__':
    unittest.main()
