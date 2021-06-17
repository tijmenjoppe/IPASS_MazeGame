"""Module containing different algorithms to generate mazes"""

import random
from maze_game.animate_helpers import *

def random_walker(maze, current_cell, path=[]):
    """random walker used in Aldolous Broder and Wilson's algorithm if chosen to use a extra walker.
    randomly walks (once per function calL) along any cells of the maze. If the cell hasn't been visited yet the passages gets carved out.
    An optional param path can be given which are positions in the maze that the random_walker can't walk on (Path from Wilson's)

    Args:
        maze:   maze object which will be used to store the generated maze.
        current_cell: position in the maze where to start our random walk from
        path: path to avoid in the random walk

    Returns:
        current_cell: if the next cell is in the path the current cell gets returned as next cell
        next_cell: the next cell to take a rand
        om step from
    """

    next_cell = maze.neighbors(current_cell[0], current_cell[1], True)[0]
    if next_cell in path:
        return current_cell
    if maze.grid[next_cell] == 1:
        maze.destroy_wall(current_cell, next_cell)
        maze.grid[next_cell] = 0

    return next_cell


def depth_first_search(maze, animate=False):
    """
    Author:
        Charles Pierre Trémaux (1876)

    Time Complexity:
        O(N) Vertices + Vertices,

    Space Complexity:
        O(N) Vertices

    Maze generation algorithm:
        (1, Difficulty: easy)

    The algorithm:
        Picks a random starting cell and carves out a passage to a random not visited neighbor cell, repeat this process from the neighbors perspective
        if ran into a dead-end return to the most previously visited position that still has not visited neighbors
        if no cells have not visited neighbors anymore the algorithm is finished

    Iterative over recursive implementation to be more memory efficient and avoid stack overflow.
    Args:
        maze: maze object which will be used to store the generated maze.
        animate: animate the generating process, 0 (=False) or FPS as integer value.
    """

    def draw():
        """Custom draw function"""
        draw_grid(win, maze.grid, tile_size)
        for pos in stack:
            pygame.draw.rect(win, RED, (pos[1] * tile_size, pos[0] * tile_size, tile_size, tile_size))
        clock.tick(animate)
        pygame.display.flip()

    if animate:
        clock, tile_size, win = animation_setup_grid(maze.grid)
    # start at the start position and mark that cell as part of the maze / visited (0)
    start = (random.randrange(1, maze.rows, 2), random.randrange(1, maze.rows, 2))

    stack = [start]
    maze.grid[start] = 0
    # while the stack has elements in it (== not all cells have been visited)
    while stack:
        # current cell is most recent cell in the stack
        current_cell = stack[-1]
        # get all not visited neighbors from the current cell (if the value in the grid is 1 the cell is not visited)
        neighbors = [n for n in maze.neighbors(current_cell[0], current_cell[1], shuffle=True) if maze.grid[n] == 1]
        # if no not visited neighbors: pop from stack
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
            draw()


def aldous_broder(maze, animate=False):
    """
    Authors:
        David Aldous, Andrei Broder

    Time Complexity:
        O(?) uses a random walker making the worst case infinite

    Space Complexity:
        O(N) Vertices.

    Maze generation algorithm:
        (5, Difficulty: hard (alternative))

    The algorithm:
        Picks a random starting cell mark it at visited and carve out a passage to a random neighbor cell, repeat this process from the neighbors perspective
        if all cells have been visited the algorithm is finished.

    Args:
        maze: maze object which will be used to store the generated maze.
        animate: animate the generating process, 0 (=False) or FPS as integer value.
    """

    def draw():
        """Custom draw function"""
        draw_grid(win, maze.grid, tile_size)
        pygame.draw.rect(win, RED,
                         (current_cell[1] * tile_size, current_cell[0] * tile_size, tile_size, tile_size))
        pygame.display.flip()
        clock.tick(animate)

    if animate:
        clock, tile_size, win = animation_setup_grid(maze.grid)

    # start a a random position and mark that cell as part of the maze / visited (0)
    current_cell = (random.randrange(1, maze.rows, 2), random.randrange(1, maze.rows, 2))
    maze.grid[current_cell] = 0

    visited = {current_cell: True}
    # while the maze contains not visited cells
    while len(visited) < maze.x*maze.y:
        # perform a random step (destroys walls and next cell if the step steps on a cell that hasn't been visited
        current_cell = random_walker(maze, current_cell)
        if visited.get(current_cell) is None:
            visited[current_cell] = True
        if animate:
            draw()


def prim(maze, animate=False):
    """
    Authors:
        Vojtěch Jarník (1930) independently rediscovered by Robert Prim (1957), Edsger Dijkstra (1959)

    Time Complexity:
        O(N) Vertices.

    Space Complexity:
        O(N) Vertices/2 + 1

    Maze generation algorithm:
        (2, Difficulty: Medium)

    The algorithm:
        Picks a random starting cell mark it at part of the maze and add all not visited neighbors to a frontier set.
        pick a random cell from the frontier set and connect it to a cell that is already part of the maze.
        mark the random cell as part of the maze and add all not visited neighbors to the frontier.
        Repeat until frontier is empty and the algorithm is finished


    Args:
        maze: maze object which will be used to store the generated maze.
        animate: animate the generating process, 0 (=False) or FPS as integer value."""

    def draw():
        """Custom draw function"""
        draw_grid(win, maze.grid, tile_size)
        for pos in frontier:
            pygame.draw.rect(win, RED, (pos[1] * tile_size, pos[0] * tile_size, tile_size, tile_size))
        pygame.display.flip()
        clock.tick(animate)

    if animate:
        clock, tile_size, win = animation_setup_grid(maze.grid)
    # set of all cells that are neighbors of cells that have been visited but not visited themself.
    frontier = set()
    start = (random.randrange(1, maze.rows, 2), random.randrange(1, maze.rows, 2))

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
            draw()


def wilson(maze, extra_walker=False, animate=False):
    """
    Author:
        David Bruce Wilson (1996)

    Time Complexity O(?):
        uses a random walker making the worst case infinite\
    Space Complexity O(N):
        Vertices.

    Maze generation algorithm:
        (4, Difficulty: Hard(alternative))

    The algorithm:
        Pick a random cell and marks it as part of the maze.
        Pick another random cell and start a random walk from it.
        if the random walk loops itself cut-off the loop and continue from there
        when the random walker walks into a cell that's already part of the maze: mark the path from the random walker part of maze
        repeat making random walkers until all cells have been visited.



    Wilson's Algorithm & Aldolous Broder hybrid
    Maze generation algorithm:
        (3, Difficulty: Hard)

    The algorithm:
        extended on Wilson. Instead of only picking a random cell and marking it as part of the maze:
        start a Random Walk from there that does destroy walls on its path (Aldolous Broder)
        this random walker avoids colliding into Wilson's path
        has a same time and space complexity as Wilson/Aldolous Broder. Though almost always faster then those by themself

    Author:
        unknown/Sjoerd Beetsma



    Args:
        maze: maze object which will be used to store the generated maze.
        extra_walker: use a extra random walker to generate the maze (aldolous broder algorithm)
        animate: animate the generating process, 0 (=False) or FPS as integer value."""

    def draw():
        """Custom draw function"""
        draw_grid(win, maze.grid, tile_size)
        for pos in path:
            pygame.draw.rect(win, RED, (pos[1] * tile_size, pos[0] * tile_size, tile_size, tile_size))
        if extra_walker:
            pygame.draw.rect(win, INDIGO,
                             (extra_walker_pos[1] * tile_size, extra_walker_pos[0] * tile_size, tile_size, tile_size))
        pygame.display.flip()

    if animate: clock, tile_size, win = animation_setup_grid(maze.grid)
    not_visited_cells = [(i, j) for i in range(1, maze.rows - 1, 2) for j in range(1, maze.cols - 1, 2)]
    # pick a random start cell
    start = random.sample(not_visited_cells, 1)[0]
    # if extra_walker is activated the walk will start from this start position
    if extra_walker:
        extra_walker_pos = start
    # remove the start position from not_visited_cells and mark it as part of the maze (0)
    not_visited_cells.remove(start)
    maze.grid[start] = 0

    # while there are not visited cells left
    while len(not_visited_cells) > 0:
        # start the path at a random location
        path = [random.sample(not_visited_cells, 1)[0]]
        # current cell is the first element in the path
        next_cell = path[0]
        # while next_cell is not part of the maze keep randomly walking (without changing the maze)
        while next_cell in not_visited_cells:
            next_cell = maze.neighbors(next_cell[0], next_cell[1], True)[0]
            # if the next_cell is in the path a loop is created cut off the path at the point of the loop and continue from there
            if next_cell in path:
                path = path[:path.index(next_cell)]
            path.append(next_cell)
            # if extra walker is active make it go a next step
            if extra_walker:
                extra_walker_pos = random_walker(maze, extra_walker_pos, path)
                # if extra walker hasn't been visited yet remove it from not visited cells
                if extra_walker_pos in not_visited_cells:
                    not_visited_cells.remove(extra_walker_pos)
            if animate:
                clock.tick(animate), draw()
        # for loop is reached when the path reaches a cell that is part of the maze(0)
        # the positions in the path and walls between them get destroyed.
        for i, pos in enumerate(path[:-1]):
            maze.grid[pos] = 0
            maze.destroy_wall(pos, path[i + 1])
            not_visited_cells.remove(pos)
        if animate:
            clock.tick(animate)
            draw()

