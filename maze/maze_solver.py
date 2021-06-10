def breadth_first_search(adj_list, start_pos, end_pos):
    # param: maze(graph) represented as adj_list

    dist_from_start = {pos: float('inf') for pos in adj_list.keys()}
    queue = [start_pos]
    dist_from_start[start_pos] = 0
    while queue:
        current = queue[0]
        queue.remove(current)
        for connected_cell in adj_list[current]:
            if dist_from_start[connected_cell] == float('inf'):
                dist_from_start[connected_cell] = dist_from_start[current] + 1
                queue.append(connected_cell)
                if connected_cell == end_pos:  # if the shortest path to target cell is found stop loop by making queue empty.
                    queue = []

    #   make the cell with the longest distance from start the end.
    #   maze.end = max(dist_from_start, key= dist_from_start.get)

    # get shortest path from end to start
    current = end_pos
    path = [current]
    #while len(path)<dist_from_start[end_pos]+1:
    while True:
        # which connection from the current point has the lowest distance? move to that direction and repeat
        # until the start of the maze is reached. (distance from start)

        # store connected cells from the current cell and their distances from start
        # {cell position: distance from start}
        connected_cells = {pos: dist_from_start[pos] for pos in adj_list[current]}
        # move to connected cell with lowest distance from start
        next_cell = (min(connected_cells, key=connected_cells.get))
        current = next_cell
        path.append(next_cell)
        if current == start_pos:
            break

    return path
