import random
import pygame
from maze.animate_helpers import draw_grid, animation_setup_grid

def random_walker(maze, current_cell, path=[]):
    """random walker used in AB and AB WILSON combination
    randomly walks along the maze and destroys the wall between the next and current cell if the next cell is not visited yet
    a path can be given to avoid (only for ab wilson)"""

    next_cell = maze.neighbors(current_cell[0], current_cell[1], True)[0]
    if next_cell in path:
        return current_cell

    if next_cell in maze.not_visited_cells.copy():
        maze.destroy_wall(current_cell, next_cell)
        maze.grid[next_cell] = 0
        maze.not_visited_cells.remove(next_cell)

    return next_cell


def depth_first_search(maze, start=(1, 1), animate=False):
    """First implemented recursively changed to iterive implementation to avoid recursion depth errors
    worst case from generating a maze based on more then 997 nodes (points on uneven rows/cols)
    O(n) n = amount of points on uneven rows/cols """
    def draw():
        draw_grid(win, maze.grid, tile_size)
        for pos in stack:
            pygame.draw.rect(win, (255, 0, 0), (pos[0] * tile_size, pos[1] * tile_size, tile_size, tile_size))
        pygame.display.flip()
    if animate:
        clock, tile_size, win = animation_setup_grid(maze.grid)

    # backtracking stack
    stack = [start]
    # default starting cell is first (uneven!) cell in the graph
    maze.grid[start] = 0
    while stack:
        # current cell
        current_cell = stack[-1]
        # find neighbors and filter out the already visited neighbors (value on graph is 0)
        neighbors = [n for n in maze.neighbors(current_cell[0], current_cell[1], True) if maze.grid[n] == 1]
        if len(neighbors) == 0:
            stack = stack[:-1]
        else:
            # make neighbor a open cell (0)
            next_cell = neighbors[0]
            maze.grid[next_cell] = 0
            # destroy wall between neighbor and current cell
            maze.destroy_wall(current_cell, next_cell)
            stack.append(next_cell)
        if animate:
            draw()
            clock.tick(animate)


def aldous_broder(maze, start=(1, 1), animate=False):
    def draw():
        draw_grid(win, maze.grid, tile_size)
        pygame.draw.rect(win, (255, 0, 0),
                         (current_cell[0] * tile_size, current_cell[1] * tile_size, tile_size, tile_size))
        pygame.display.flip()
    if animate:
        clock, tile_size, win = animation_setup_grid(maze.grid)
    # ---------------------
    current_cell = start
    maze.grid[current_cell] = 0
    maze.not_visited_cells.remove(current_cell)
    while len(maze.not_visited_cells) > 0:
        current_cell = random_walker(maze, current_cell)
        # ---------------------
        if animate:
            draw()
            clock.tick(animate)

def prim(maze, start=(1,1), animate=False):
    def draw():
        draw_grid(win, maze.grid, tile_size)
        for pos in frontier:
            pygame.draw.rect(win, (255, 0, 0), (pos[0] * tile_size, pos[1] * tile_size, tile_size, tile_size))
    if animate:
        clock, tile_size, win = animation_setup_grid(maze.grid)
    # ---------------------
    frontier = set()
    maze.grid[start] = 0
    for cell in maze.neighbors(start[0], start[1]):
        frontier.add(cell)
    while frontier:
        random_front = random.sample(frontier, 1)[0]
        connected_cell = [n for n in maze.neighbors(random_front[0], random_front[1]) if maze.grid[n] == 0]
        maze.destroy_wall(connected_cell[0], random_front)
        maze.grid[random_front] = 0
        new_fronts = [n for n in maze.neighbors(random_front[0], random_front[1]) if maze.grid[n] == 1]
        for front in new_fronts:
            frontier.add(front)
        frontier.remove(random_front)
        # ---------------------
        if animate:
            draw()
            clock.tick(animate)
            pygame.display.flip()
def wilson(maze, start=(1, 1), animate=False, extra_walker = False):
    def draw():
        draw_grid(win, maze.grid, tile_size)
        for pos in path:
            pygame.draw.rect(win, (255, 0, 0), (pos[0] * tile_size, pos[1] * tile_size, tile_size, tile_size))
        if extra_walker:
            pygame.draw.rect(win, (255, 0, 0),
                             (extra_walker_pos[0] * tile_size, extra_walker_pos[1] * tile_size, tile_size, tile_size))
        pygame.display.flip()

    if animate:
        clock, tile_size, win = animation_setup_grid(maze.grid)
    start = random.sample(maze.not_visited_cells, 1)[0]
    extra_walker_pos = start
    maze.not_visited_cells.remove(start)
    maze.grid[start] = 0

    while len(maze.not_visited_cells) > 0:
        path = [random.sample(maze.not_visited_cells, 1)[0]]
        next_cell = path[-1]

        while next_cell in maze.not_visited_cells:
            next_cell = maze.neighbors(next_cell[0], next_cell[1], True)[0]
            if next_cell in path:
                path = path[:path.index(next_cell)]
            path.append(next_cell)
            if extra_walker:
                extra_walker_pos = random_walker(maze, extra_walker_pos, path)

            if animate:
                clock.tick(animate)
                draw()

        for i, pos in enumerate(path[:-1]):
            maze.grid[pos] = 0
            maze.destroy_wall(pos, path[i + 1])
            maze.not_visited_cells.remove(pos)