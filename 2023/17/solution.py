import lib.aoc
import lib.graph
import lib.grid

def generate_heuristic_to_end_node(grid):
    def heuristic_neighbor(state):
        x, y = state
        for n in [(x-1,y), (x+1,y),
                  (x,y-1), (x,y+1)]:
            if n in grid:
                yield n, grid[x,y]

    heuristic_graph = lib.graph.make_lazy_graph(heuristic_neighbor)

    heuristic = dict(lib.graph.all_reachable(heuristic_graph,
                                             (grid.width-1,
                                              grid.height-1)))
    heuristic[grid.width-1, grid.height-1] = 0
    return heuristic.__getitem__

def solve(s, min_steps, max_steps):
    grid = lib.grid.FixedGrid.parse(s, value_fn=int)

    # Avoid repeatedly calling the property getter for performance
    g_width, g_height = grid.width, grid.height

    def neighbor_fn(state):
        x, y, dx, dy, num_in_dir = state

        if num_in_dir < max_steps:
            nx, ny = x+dx, y+dy
            if 0 <= nx < g_width and 0 <= ny < g_height:
                new_state = (nx, ny, dx, dy, num_in_dir+1)
                yield new_state, grid[nx,ny]

        if num_in_dir >= min_steps:
            # Left turn
            nx, ny = x+dy, y-dx
            if 0 <= nx < g_width and 0 <= ny < g_height:
                new_state = (nx, ny, dy, -dx, 1)
                yield new_state, grid[nx,ny]

            # Right turn
            nx, ny = x-dy, y+dx
            if 0 <= nx < g_width and 0 <= ny < g_height:
                new_state = (nx, ny, -dy, dx, 1)
                yield new_state, grid[nx,ny]

    graph = lib.graph.make_lazy_graph(neighbor_fn)

    def end_fn(state):
        x, y, _, _, num_in_dir = state
        return (x == g_width-1 and
                y == g_height-1 and
                num_in_dir >= min_steps)

    heuristic_to_end = generate_heuristic_to_end_node(grid)

    def heuristic(state):
        x, y, _, _, _ = state
        return heuristic_to_end((x,y))

    return lib.graph.dijkstra_length_fuzzy_end(graph,
                                               [(0, 0, 1, 0, 0),
                                                (0, 0, 0, 1, 0)],
                                               end_fn=end_fn,
                                               heuristic=heuristic)

def part1(s):
    answer = solve(s, 0, 3)

    lib.aoc.give_answer(2023, 17, 1, answer)

def part2(s):
    answer = solve(s, 4, 10)

    lib.aoc.give_answer(2023, 17, 2, answer)

INPUT = lib.aoc.get_input(2023, 17)
part1(INPUT)
part2(INPUT)
