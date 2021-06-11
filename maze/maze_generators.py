import random
import pygame
def animation_setup_grid(grid, tile_size=10):
    pygame.init()
    clock = pygame.time.Clock()
    tile_size = tile_size
    win = pygame.display.set_mode((len(grid)*tile_size, len(grid[0])*tile_size))

    return clock, tile_size, win
def draw_grid(win,grid, tile_size):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    cols = len(grid[0])
    rows = len(grid)
    for Y in range(cols):
        for X in range(rows):
            x = X * tile_size
            y = Y * tile_size
            if grid[X][Y] == 1:
                pygame.draw.rect(win, (0, 0, 0), (y, x, tile_size, tile_size))
            elif grid[X][Y] == 0:
                pygame.draw.rect(win, (255,255, 255), (y, x, tile_size, tile_size))

def depth_first_search(maze, start=(1, 1), animate=False):
    """First implemented recursively changed to iterive implementation to avoid recursion depth errors
    worst case from generating a maze based on more then 997 nodes (points on uneven rows/cols)
    O(n) n = amount of points on uneven rows/cols """
    def draw():
        draw_grid(win, maze.grid, tile_size)
        for pos in stack:
            pygame.draw.rect(win, (255, 0, 0), (pos[1] * tile_size, pos[0] * tile_size, tile_size, tile_size))
        pygame.display.flip()
    if animate:
        clock, tile_size, win = animation_setup_grid(maze.grid)

    # backtracking stack
    stack = [start]
    # default starting cell is first (uneven!) cell in the graph
    maze.grid[start] = 0
    while stack:
        if animate:
            draw()
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


def aldous_broder(maze, start=(1, 1), animate=False):
    def draw():
        draw_grid(win, maze.grid, tile_size)
        pygame.draw.rect(win, (0, 255, 0),
                         (current_cell[1] * tile_size, current_cell[0] * tile_size, tile_size, tile_size))
        pygame.display.flip()
    if animate:
        clock, tile_size, win = animation_setup_grid(maze.grid)

    visited_cells = [start]
    current_cell = start
    maze.grid[current_cell] = 0
    while len(visited_cells) < (maze.x * maze.y):
        if animate:
            draw()
        neighbors = maze.neighbors(current_cell[0], current_cell[1], True)
        next_cell = neighbors[0]
        if maze.grid[next_cell]:
            visited_cells.append(next_cell)
            maze.destroy_wall(current_cell, next_cell)
            maze.grid[next_cell] = 0
        current_cell = next_cell

def prim(maze, start=(1, 1), animate=False):
    print("prim")
    def draw():
        draw_grid(win, maze.grid, tile_size)
        for pos in frontier:
            pygame.draw.rect(win, (255, 0, 0), (pos[1] * tile_size, pos[0] * tile_size, tile_size, tile_size))
        pygame.display.flip()

    if animate:
        clock, tile_size, win = animation_setup_grid(maze.grid)
    frontier = set()
    maze.grid[start] = 0
    for cell in maze.neighbors(start[0], start[1]):
        frontier.add(cell)
    while frontier:
        if animate:
            draw()
        random_front = random.sample(frontier, 1)[0]
        connected_cell = [n for n in maze.neighbors(random_front[0], random_front[1]) if maze.grid[n] == 0]
        maze.destroy_wall(connected_cell[0], random_front)
        maze.grid[random_front] = 0
        new_fronts = [n for n in maze.neighbors(random_front[0], random_front[1]) if maze.grid[n] == 1]
        for front in new_fronts:
            frontier.add(front)
        frontier.remove(random_front)


