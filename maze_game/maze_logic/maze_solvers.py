"""Module containing different algorithms to solve mazes"""

from maze_game.animate_helpers import *

def breadth_first_search(maze, start_pos, animate=False):
    """
    Authors: Konrad Zuse (1945), Edward F. Moore (1959)

    Time Complexity O(N): Vertices + Edges

    Space Complexity O(N): Vertices + Edges

    The Algorithm:
        starts at a given start cell and spreads out to not visited neighboring cells marking their distance from the start cell
        these neighbor cells repeat the process until the end of the maze is found then the algorithm
        travels back the shortest path to the start end stores it's path

    Args:
        maze:   maze object which will be used to store the generated maze.
        start_pos: position in the maze where to start the pathfinding from
        animate: animate the generating process, False or FPS as integer value.

    Returns:
        the shortest path from start_position the the maze end in the form of a list with grid positions
        example: [(1,1),(2,1),...(5,5)]
        """

    def draw():
        """custom draw function"""
        draw_grid(win, maze.grid, tile_size)
        for pos in [pos for pos in dist_from_start if dist_from_start[pos] != float('inf')]:
            pygame.draw.rect(win, BLUE, (pos[1] * tile_size, pos[0] * tile_size, tile_size, tile_size))
        draw_start_finish(win, tile_size, start_pos, maze.end)
        clock.tick(animate)
        pygame.display.flip()

    if animate:
        clock, tile_size, win = animation_setup_grid(maze.grid)
        draw_grid(win, maze.grid, tile_size)
    # adj_lst is a @property so store it in a separate variable to not generate the same adj_lst over and over.
    adj_lst = maze.adj_lst
    # each cell's distance from the start used to traverse the graph and also check if cells have been visited
    # (dist != inf)
    dist_from_start = {pos: float('inf') for pos in adj_lst.keys()}
    # queue data type to store which cells to visit next
    queue = [start_pos]
    # start cell has a distance of 0 to start cell
    dist_from_start[start_pos] = 0

    # while the queue is not empty
    while queue:
        current = queue[0]
        queue.remove(current)
        # for each connected open (0) cell to the current cell
        for connected_cell in adj_lst[current]:
            # if not visited
            if dist_from_start[connected_cell] == float('inf'):
                # store distances of the connected cell and add to queue
                dist_from_start[connected_cell] = dist_from_start[current] + 1
                queue.append(connected_cell)
                # if the shortest path to target cell is found stop loop by making queue empty.
                if connected_cell == maze.end:
                    queue = []
                    break
        if animate:
            draw()

    # get shortest path from end to start by traversing the graph from the and and going to the cell with the shortest
    # distance from start
    current = maze.end
    path = [current]

    while True:
        # which connection from the current point has the lowest distance? move to that direction and repeat
        # until the start of the maze is reached. (distance from start)
        # store connected cells from the current cell and their distances from start
        # {cell position: distance from start}
        connected_cells = {pos: dist_from_start[pos] for pos in adj_lst[current]}
        # move to connected cell with lowest distance from start
        next_cell = (min(connected_cells, key=connected_cells.get))
        current = next_cell
        path.append(next_cell)
        if current == start_pos:
            break
    # reverse the path so path becomes in order [start, ... , end]
    path.reverse()
    if animate:
        for pos in path[1:-1]:
            pygame.draw.rect(win, INDIGO, (pos[1] * tile_size, pos[0] * tile_size, tile_size, tile_size))
        pygame.display.flip()
    return path


def depth_first_search(maze, start_pos, animate=False):
    """
    Author: Charles Pierre Trémaux (1876)

    Time Complexity O(N): Vertices + Edges

    Space Complexity O(N): Vertices + Edges

    The algorithm:
        starts at a given start cell spreading out to a random not visited neighboring cell and storing it's path
        these neighbor cells repeat the process until the end of the maze is found.
        if the path runs into a dead-end it will go back until it can spread to not visited neighbors again

    Args:
        maze:   maze object which will be used to store the generated maze.
        start_pos: position in the maze where to start the pathfinding from
        animate: animate the generating process, False or FPS as integer value.

    Returns:
        path from start_position the the maze end in the form of a list with grid positions
        example: [(1,1),(2,1),...(5,5)]
    """

    def draw(stack_color=BLUE):
        draw_grid(win, maze.grid, tile_size)
        for pos in stack:
            pygame.draw.rect(win, stack_color, (pos[1] * tile_size, pos[0] * tile_size, tile_size, tile_size))
        draw_start_finish(win, tile_size, start_pos, maze.end)
        clock.tick(animate)
        pygame.display.flip()

    if animate:
        clock, tile_size, win = animation_setup_grid(maze.grid)
    # stack to store the last steps taken to go back when running into a dead-end
    stack = [start_pos]
    # adj_lst is a @property so store it in a separate variable to not generate the same adj_lst over and over.
    adj_lst = maze.adj_lst
    visited = {start_pos: True}
    # continue until a path is found and return stack(==path) or stack is empty (no solution and return none)
    while stack:
        # current cell is most recent element appended to the stack
        current_cell = stack[-1]
        # if maze end is found
        if current_cell == maze.end:
            # draw the path in the non-standard color to make the solution a different color when animating
            if animate:
                draw(INDIGO)
            return stack
        # get neighbors/connected open cells(0) that haven't been visited yet
        unvisited_neighbors = [connected_cell for connected_cell in adj_lst[current_cell] if
                               visited.get(connected_cell) is None]
        # if there are none pop from stack
        if len(unvisited_neighbors) == 0:
            stack = stack[:-1]
        # a random unvisited neighbor becomes the next cell
        else:
            next_cell = unvisited_neighbors[0]
            stack.append(next_cell)
            visited[next_cell] = True
        if animate:
            draw()
