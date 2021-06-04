
def depth_first_search(maze, start=(1, 1)):
    # backtracking stack
    stack = [start]
    # default starting cell is first (uneven!) cell in the graph
    maze.graph[start] = 0
    while stack:
        # current cell
        current_cell = stack[-1]
        # find neighbors and filter out the already visited neighbors (value on graph is 0)
        neighbors = [n for n in maze.neighbors(current_cell[0], current_cell[1], True) if maze.graph[n] == 1]
        if len(neighbors) == 0:
            stack = stack[:-1]
        else:
            # make neighbor a open cell (0)
            next_cell = neighbors[0]
            maze.graph[next_cell] = 0
            # destroy wall between neighbor and current cell
            maze.destroy_wall(current_cell, next_cell)
            stack.append(next_cell)


def aldous_broder(maze, start=(1, 1)):
    visited_cells = [start]
    current_cell = start
    while len(visited_cells) < (maze.x * maze.y):
        maze.graph[current_cell] = 0
        neighbors = maze.neighbors(current_cell[0], current_cell[1], True)
        print(neighbors)
        next_cell = neighbors[0]
        if maze.graph[next_cell]:
            visited_cells.append(next_cell)
            maze.destroy_wall(current_cell, next_cell)
            maze.graph[next_cell] = 0
        current_cell = next_cell