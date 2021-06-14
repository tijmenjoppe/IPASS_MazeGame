import random
import pygame
from maze.animate_helpers import draw_grid, animation_setup_grid
from rgb_colors import *


def random_walker(maze, current_cell, path=[]):
    """random walker used in Aldolous Broder and Wilson's algorithm if chosen to use a extra walker.
    randomly walks (once per function calL) along any cells of the maze. If the cell hasn't been visited yet the passages gets carved out.
    An optional param path can be given which are positions in the maze that the random_walker can't walk on (Path from wilson's)
    Args:
        maze:   maze object which will be used to store the generated maze.
        current_cell: position in the maze where to start our random walk from
        path: path to avoid in the random walk
    Returns:
        current_cell: if the next cell is in the path the current cell gets returned as next cell
        next_cell: the next cell to take a random step from
    """

    next_cell = maze.neighbors(current_cell[0], current_cell[1], True)[0]
    if next_cell in path:
        return current_cell
    if next_cell in maze.not_visited_cells.copy():
        maze.destroy_wall(current_cell, next_cell)
        maze.grid[next_cell] = 0
        maze.not_visited_cells.remove(next_cell)
    return next_cell


def depth_first_search(maze, start=(1, 1), animate=False):
    """ Maze generation algorithm: Depth First Search, difficulty: 1. Algo Nr: 1

    First implemented recursively changed to iterive implementation to avoid recursion depth errors
    worst case from generating a maze based on more then 997 nodes (points on uneven rows/cols)
    O(n) n = amount of nodes
    Args:
        maze: maze object which will be used to store the generated maze.
        start: starting position of the algorithm.
        animate: animate the generating process, False or FPS as integer value.
    """

    def draw():
        """Custom draw function"""
        draw_grid(win, maze.grid, tile_size)
        for pos in stack:
            pygame.draw.rect(win, RED, (pos[0] * tile_size, pos[1] * tile_size, tile_size, tile_size))
        pygame.display.flip()

    if animate:
        clock, tile_size, win = animation_setup_grid(maze.grid)
    # start at the start position and mark that cell as part of the maze / visited (0)
    stack = [start]
    maze.grid[start] = 0
    # while the stack has elements in it (== not all cells have been visited)
    while stack:
        # current cell is most recent cell in the stack
        current_cell = stack[-1]
        # get all unvisited neighbors from the current cell (if the value in the grid is 1 the cell is unvisited)
        neighbors = [n for n in maze.neighbors(current_cell[0], current_cell[1], shuffle=True) if maze.grid[n] == 1]
        # if no unvisited neighbors: pop from stack
        if len(neighbors) == 0:
            stack = stack[:-1]
        # else make a random neighbor the next cell destroy the wall between the current and next cell,
        # and mark it as part of the maze (0) and add to stack
        else:
            next_cell = neighbors[0]
            maze.grid[next_cell] = 0
            stack.append(next_cell)
            # destroy wall between current cell and next cell
            maze.destroy_wall(current_cell, next_cell)

        if animate:
            draw(), clock.tick(animate)


def aldous_broder(maze, start=(1, 1), animate=False):
    """
    Maze generation algorithm: Aldous Broder, Difficulty: 3 (alt). Algo Nr: 5
    Args:
        maze: maze object which will be used to store the generated maze.
        start: starting position of the algorithm.
        animate: animate the generating process, False or FPS as integer value."""

    def draw():
        """Custom draw function"""
        draw_grid(win, maze.grid, tile_size)
        pygame.draw.rect(win, RED,
                         (current_cell[0] * tile_size, current_cell[1] * tile_size, tile_size, tile_size))
        pygame.display.flip()

    if animate:
        clock, tile_size, win = animation_setup_grid(maze.grid)
    # start at the start position and mark that cell as part of the maze / visited (0)
    current_cell = start
    maze.grid[current_cell] = 0
    maze.not_visited_cells.remove(current_cell)
    # while the maze contains unvisited cells
    while len(maze.not_visited_cells) > 0:
        # perform a random step (destroys walls and next cell if the step steps on a cell that hasn't been visited
        current_cell = random_walker(maze, current_cell)
        if animate:
            draw()
            clock.tick(animate)


def prim(maze, start=(1, 1), animate=False):
    """
    Maze generation algorithm: Prim's algorithm, Difficulty: 2. Algo Nr: 2
    Args:
        maze: maze object which will be used to store the generated maze.
        start: starting position of the algorithm.
        animate: animate the generating process, False or FPS as integer value."""

    def draw():
        """Custom draw function"""
        draw_grid(win, maze.grid, tile_size)
        for pos in frontier:
            pygame.draw.rect(win, RED, (pos[0] * tile_size, pos[1] * tile_size, tile_size, tile_size))
        pygame.display.flip()

    if animate:
        clock, tile_size, win = animation_setup_grid(maze.grid)
    # set of all cells that are neighbors of cells that have been visited but not visited themself.
    frontier = set()
    # start at the start position and mark that cell as part of the maze / visited (0)
    maze.grid[start] = 0
    # add the neighbors of the starting cell to the frontier
    for cell in maze.neighbors(start[0], start[1]):
        frontier.add(cell)
    # algorithm finishes when frontier is empty: all cells have been visited.
    while frontier:
        # choose a random next cell from the frontier
        random_frontier_cell = random.sample(frontier, 1)[0]
        # get a cell that is already in the maze and is also a neighbor of the frontier cell
        connected_cell = [n for n in maze.neighbors(random_frontier_cell[0], random_frontier_cell[1]) if maze.grid[n] == 0]
        # destroy wall between current cell and next cell and mark the random frontier cell as part of the maze (0)
        maze.destroy_wall(connected_cell[0], random_frontier_cell)
        maze.grid[random_frontier_cell] = 0
        # get neighbor cells of the random frontier cell that aren't in the maze yet and add them to the frontier.
        new_fronts = [n for n in maze.neighbors(random_frontier_cell[0], random_frontier_cell[1]) if maze.grid[n] == 1]
        for front in new_fronts:
            frontier.add(front)
        frontier.remove(random_frontier_cell)

        if animate:
            draw(), clock.tick(animate)


def wilson(maze, extra_walker=False, animate=False):
    """
    Maze generation algorithm: Wilson's algorithm, Difficulty: 3 (alt). Algo Nr: 4
    and optionally combines Wilson's Algorithm with Aldolous Broder, Difficulty: 3 (main). Algo Nr: 3

    Args:
        maze: maze object which will be used to store the generated maze.
        extra_walker: use a extra random walker to generate the maze (aldolous broder algorithm)
        animate: animate the generating process, False or FPS as integer value."""

    def draw():
        """Custom draw function"""
        draw_grid(win, maze.grid, tile_size)
        for pos in path:
            pygame.draw.rect(win, RED, (pos[0] * tile_size, pos[1] * tile_size, tile_size, tile_size))
        if extra_walker:
            pygame.draw.rect(win, RED,
                             (extra_walker_pos[0] * tile_size, extra_walker_pos[1] * tile_size, tile_size, tile_size))
        pygame.display.flip()

    if animate: clock, tile_size, win = animation_setup_grid(maze.grid)
    # pick a random start cell
    start = random.sample(maze.not_visited_cells, 1)[0]
    # if extra_walker is activated the walk will start from this start position
    if extra_walker:
        extra_walker_pos = start
    # remove the start position from not_visited_cells and mark it as part of the maze (0)
    maze.not_visited_cells.remove(start)
    maze.grid[start] = 0

    # while there are unvisited cells left
    while len(maze.not_visited_cells) > 0:
        # start the path at a random location
        path = [random.sample(maze.not_visited_cells, 1)[0]]
        # current cell is the first element in the path
        next_cell = path[0]
        # while next_cell is not part of the maze keep randomly walking (without changing the maze)
        while next_cell in maze.not_visited_cells:
            next_cell = maze.neighbors(next_cell[0], next_cell[1], True)[0]
            # if the next_cell is in the path a loop is created cut off the path at the point of the loop and continue from there
            if next_cell in path:
                path = path[:path.index(next_cell)]
            path.append(next_cell)
            # if extra walker is active make it go a next step
            if extra_walker:
                extra_walker_pos = random_walker(maze, extra_walker_pos, path)
            if animate:
                clock.tick(animate), draw()
        # for loop is reached when the path reaches a cell that is part of the maze(0)
        # the positions in the path and walls between them get destroyed.
        for i, pos in enumerate(path[:-1]):
            maze.grid[pos] = 0
            maze.destroy_wall(pos, path[i + 1])
            maze.not_visited_cells.remove(pos)
