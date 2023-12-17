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

    # This graph *always* turns at every node. To compensate, every possible
    # number of forward steps is returned as an option for each state
    # Overall this actually reduces the state space a good bit!
    def neighbor_fn(state):
        x, y, horizontal = state

        if horizontal:
            # Turning to vertical
            for ndy in (1, -1):
                ny = y
                cost = 0
                for steps in range(1, max_steps+1):
                    ny += ndy
                    if 0 <= ny < g_height:
                        cost += grid[x,ny]
                        if steps >= min_steps:
                            new_state = (x, ny, False)
                            yield new_state, cost
                    else:
                        break
        else:
            # Turning to horizontal
            for ndx in (1, -1):
                nx = x
                cost = 0
                for steps in range(1, max_steps+1):
                    nx += ndx
                    if 0 <= nx < g_width:
                        cost += grid[nx,y]
                        if steps >= min_steps:
                            new_state = (nx, y, True)
                            yield new_state, cost
                    else:
                        break

    graph = lib.graph.make_lazy_graph(neighbor_fn)

    def end_fn(state):
        x, y, _= state
        return (x == g_width-1 and
                y == g_height-1)

    heuristic_to_end = generate_heuristic_to_end_node(grid)

    def heuristic(state):
        x, y, horizontal = state
        return heuristic_to_end((x,y))

    return lib.graph.dijkstra_length_fuzzy_end(graph,
                                               [(0, 0, True),
                                                (0, 0, False)],
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
