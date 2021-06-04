import random

def depth_first_search(maze, start=(1, 1)):
    """First implemented recursively changed to iterive implementation to avoid recursion depth errors
    worst case from generating a maze based on more then 997 nodes (points on uneven rows/cols)
    O(n) n = amount of points on uneven rows/cols """
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


def aldous_broder(maze, start=(1, 1)):
    visited_cells = [start]
    current_cell = start
    while len(visited_cells) < (maze.x * maze.y):
        maze.grid[current_cell] = 0
        neighbors = maze.neighbors(current_cell[0], current_cell[1], True)
        print(neighbors)
        next_cell = neighbors[0]
        if maze.grid[next_cell]:
            visited_cells.append(next_cell)
            maze.destroy_wall(current_cell, next_cell)
            maze.grid[next_cell] = 0
        current_cell = next_cell


def prim(maze, start=(1, 1)):
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


# just for testing purposes
if __name__ == '__main__':
    from maze import Maze

    m = Maze(3, 3)
    prim(m)
