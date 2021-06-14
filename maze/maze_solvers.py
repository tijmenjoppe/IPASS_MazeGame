import pygame
from maze.animate_helpers import *


def breadth_first_search(maze, start_pos, animate=False):

    if animate:
        clock, tile_size, win = animation_setup_grid(maze.grid)
        draw_grid(win, maze.grid, tile_size)
    # param: maze(graph) represented as adj_list
    dist_from_start = {pos: float('inf') for pos in maze.adj_lst.keys()}
    queue = [start_pos]
    dist_from_start[start_pos] = 0
    while queue:
        current = queue[0]
        queue.remove(current)
        for connected_cell in maze.adj_lst[current]:
            if dist_from_start[connected_cell] == float('inf'):
                dist_from_start[connected_cell] = dist_from_start[current] + 1
                queue.append(connected_cell)


                if connected_cell == maze.end:  # if the shortest path to target cell is found stop loop by making queue empty.
                    queue = []
        if animate:
            draw_grid(win, maze.grid, tile_size)
            for pos in [pos for pos in dist_from_start if dist_from_start[pos] != float('inf')]:
                pygame.draw.rect(win, BLUE, (pos[0] * tile_size, pos[1] * tile_size, tile_size, tile_size))
            clock.tick(animate)
            pygame.display.flip()

    #   make the cell with the longest distance from start the end.
    #   maze.end = max(dist_from_start, key= dist_from_start.get)

    # get shortest path from end to start
    current = maze.end
    path = [current]
    # while len(path)<dist_from_start[end_pos]+1:
    while True:
        # which connection from the current point has the lowest distance? move to that direction and repeat
        # until the start of the maze is reached. (distance from start)

        # store connected cells from the current cell and their distances from start
        # {cell position: distance from start}
        connected_cells = {pos: dist_from_start[pos] for pos in maze.adj_lst[current]}
        # move to connected cell with lowest distance from start
        next_cell = (min(connected_cells, key=connected_cells.get))
        current = next_cell
        path.append(next_cell)
        if current == start_pos:
            break
    path.reverse()
    return path


def depth_first_search(maze, start_pos, animate=False):
    if animate:
        clock, tile_size, win = animation_setup_grid(maze.grid)
    stack = [start_pos]
    visited = [start_pos]
    while True:
        # current cell
        current_cell = stack[-1]
        if current_cell == maze.end:
            return stack
        unvisited_neighbors = [connected_cell for connected_cell in maze.adj_lst[current_cell].copy() if
                               connected_cell not in visited]
        if len(unvisited_neighbors) == 0:
            stack = stack[:-1]
        else:
            next_cell = unvisited_neighbors[0]
            stack.append(next_cell)
            visited.append(next_cell)
            if animate:
                draw_grid(win, maze.grid, tile_size)
                for pos in stack:
                    pygame.draw.rect(win, BLUE, (pos[0] * tile_size, pos[1] * tile_size, tile_size, tile_size))
                clock.tick(animate)
                pygame.display.flip()

