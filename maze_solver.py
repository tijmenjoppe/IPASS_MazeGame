def breadth_first_search(adj_list, start_pos, end_pos):
    # param: maze(graph) represented as adj_list

    visited = {pos: False for pos in adj_list.keys()}
    # 999.... represents infinite
    dist_from_start = {pos: 99999999 for pos in adj_list.keys()}
    queue = [start_pos]
    dist_from_start[start_pos] = 0
    visited[start_pos] = True

    while queue:
        current = queue[0]
        queue.remove(current)
        for connected_cell in adj_list[current]:
            if not visited[connected_cell]:
                visited[connected_cell] = True
                dist_from_start[connected_cell] = dist_from_start[current] + 1
                queue.append(connected_cell)

    #   make the cell with the longest distance from start the end.

    #   maze.end = max(dist_from_start, key= dist_from_start.get)

    # get shortest path from end to start
    current = end_pos
    path = [current]
    while True:
        # which connection from the current point has the lowest distance? move to that direction and repeat
        # until the start of the maze is reached.
        d= {pos: dist_from_start[pos] for pos in adj_list[current]}
        next = (min(d, key=d.get))
        current = next
        path.append(next)
        if current == start_pos:
            break
    return path

