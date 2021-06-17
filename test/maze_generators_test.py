import unittest
import numpy as np
from maze_game.maze_logic.maze import Maze


# helper function for testing maze generators
def perfect_maze_check(maze):
    """test if a maze object contains a perfect maze by a counting the number of open (0) cells
    then use a flood fill heuristic
    if the flood fill encounters cells that are already in the flood fill the maze contains loops != perfect
    if after the flood fill the amount of flood filled cells is less then the amount of open cells (0) in the maze
    the maze contains closed off areas != perfect
    uses recursion because of this it's recommended to only test mazes upto 20x20 == 41*41 (wall and normal cells)
    if any of the (implemented!) generation algorithms works upto 30x30 it can be suggested it will work with any size maze.
    args:
        maze: Maze object
    returns:
        True if Maze object is a perfect maze.
        False if maze object is not a perfect maze."""
    # count all open cells with for loop through the grid
    open_cell_count = np.count_nonzero(maze.grid == 0)

    def flood(flooded_cells=[], current_cell=(1, 1)):
        if current_cell in flooded_cells:
            return False
        flooded_cells.append(current_cell)
        open_cell_neighbors = [n for n in maze.neighbors(current_cell[0], current_cell[1], radius=1) if
                               not maze.grid[n] and n not in flooded_cells]
        if len(open_cell_neighbors) == 0:
            return flooded_cells
        for neighbor in open_cell_neighbors:
            flooded_cells = flood(flooded_cells=flooded_cells, current_cell=neighbor)
        return flooded_cells

    flooded_cells = flood()
    if not flooded_cells:
        return False
    elif len(flooded_cells) != open_cell_count or not flooded_cells:
        return False
    return True


class TestMazeGenerators(unittest.TestCase):
    """Test class for testing maze_generators.py
    by testing if the algorithms result in a perfect maze."""
    # test perfect maze checker has to work to check if mazes are perfect
    def test_perfect_maze_checker(self):
        maze = Maze(3, 3)
        # valid maze
        maze.grid = np.array([[1, 1, 1, 1, 1, 1, 1],
                              [1, 0, 1, 0, 1, 0, 1],
                              [1, 0, 1, 0, 1, 0, 1],
                              [1, 0, 0, 0, 1, 0, 1],
                              [1, 0, 1, 0, 1, 0, 1],
                              [1, 0, 1, 0, 0, 0, 1],
                              [1, 1, 1, 1, 1, 1, 1]])
        self.assertEqual(perfect_maze_check(maze), True)
        # invalid maze because top left corner there is a loop
        maze.grid = np.array([[1, 1, 1, 1, 1, 1, 1],
                              [1, 0, 0, 0, 1, 0, 1],
                              [1, 0, 1, 0, 1, 0, 1],
                              [1, 0, 0, 0, 1, 0, 1],
                              [1, 0, 1, 0, 1, 0, 1],
                              [1, 0, 1, 0, 0, 0, 1],
                              [1, 1, 1, 1, 1, 1, 1]])
        self.assertEqual(perfect_maze_check(maze), False)
        # invalid maze because top right corner there a partition blocked off
        maze.grid = np.array([[1, 1, 1, 1, 1, 1, 1],
                              [1, 0, 1, 0, 1, 0, 1],
                              [1, 0, 1, 0, 1, 0, 1],
                              [1, 0, 0, 0, 1, 1, 1],
                              [1, 0, 1, 0, 1, 0, 1],
                              [1, 0, 1, 0, 0, 0, 1],
                              [1, 1, 1, 1, 1, 1, 1]])
        self.assertEqual(perfect_maze_check(maze), False)

    # Depth first search
    def test_is_DFS_perfect(self):
        maze = Maze(3, 3, 1)
        self.assertEqual(perfect_maze_check(maze), True)
        maze = Maze(20, 20, 1)
        self.assertEqual(perfect_maze_check(maze), True)

    # Prim
    def test_is_Prim_perfect(self):
        maze = Maze(3, 3, 2)
        self.assertEqual(perfect_maze_check(maze), True)
        maze = Maze(20, 20, 2)
        self.assertEqual(perfect_maze_check(maze), True)

    # Wilson in combination with Aldolous Broder
    def test_is_WilsonAB_perfect(self):
        maze = Maze(3, 3, 3)
        self.assertEqual(perfect_maze_check(maze), True)
        maze = Maze(20, 20, 3)
        self.assertEqual(perfect_maze_check(maze), True)

    # Wilson
    def test_is_Wilson_perfect(self):
        maze = Maze(3, 3, 4)
        self.assertEqual(perfect_maze_check(maze), True)
        maze = Maze(20, 20, 4)
        self.assertEqual(perfect_maze_check(maze), True)

    # Aldolous Broder
    def test_is_AB_perfect(self):
        maze = Maze(3, 3, 5)
        self.assertEqual(perfect_maze_check(maze), True)
        maze = Maze(20, 20, 5)
        self.assertEqual(perfect_maze_check(maze), True)


if __name__ == '__main__':
    unittest.main()
