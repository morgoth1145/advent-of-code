import lib.aoc
import lib.graph
import lib.grid

def part1(s):
    grid = lib.grid.FixedGrid.parse(s, value_fn=int)

    def neighbor_fn(state):
        x, y, dx, dy, num_in_dir = state

        for n in [(x-1, y),
                  (x+1, y),
                  (x, y-1),
                  (x, y+1)]:
            ndx = n[0] - x
            ndy = n[1] - y
            if ndx == dx and ndy == dy:
                if num_in_dir == 3:
                    continue
                new_num_in_dir = num_in_dir+1
            elif ndx == -dx and ndx != 0:
                continue
            elif ndy == -dy and ndy != 0:
                continue
            else:
                new_num_in_dir = 1

            if 0 <= n[0] < grid.width:
                if 0 <= n[1] < grid.height:
                    new_state = (n[0], n[1],
                                 ndx, ndy,
                                 new_num_in_dir)
                    yield new_state, grid[n]

    graph = lib.graph.make_lazy_graph(neighbor_fn)

    def end_fn(state):
        x, y, _, _, _ = state
        win = (x == grid.width-1 and y == grid.height-1)
        return win

    answer = lib.graph.dijkstra_length_fuzzy_end(graph,
                                                 (0, 0,
                                                  0, 0,
                                                  0),
                                                 end_fn=end_fn)

    lib.aoc.give_answer(2023, 17, 1, answer)

def part2(s):
    grid = lib.grid.FixedGrid.parse(s, value_fn=int)

    def neighbor_fn(state):
        x, y, dx, dy, num_in_dir = state

        for n in [(x-1, y),
                  (x+1, y),
                  (x, y-1),
                  (x, y+1)]:
            ndx = n[0] - x
            ndy = n[1] - y
            if ndx == dx and ndy == dy:
                if num_in_dir == 10:
                    continue
                new_num_in_dir = num_in_dir+1
            elif ndx == -dx and ndx != 0:
                continue
            elif ndy == -dy and ndy != 0:
                continue
            else:
                if num_in_dir < 4:
                    continue
                new_num_in_dir = 1

            if 0 <= n[0] < grid.width:
                if 0 <= n[1] < grid.height:
                    new_state = (n[0], n[1],
                                 ndx, ndy,
                                 new_num_in_dir)
                    yield new_state, grid[n]

    graph = lib.graph.make_lazy_graph(neighbor_fn)

    def end_fn(state):
        x, y, _, _, _ = state
        win = (x == grid.width-1 and y == grid.height-1)
        return win

    answer = lib.graph.dijkstra_length_fuzzy_end(graph,
                                                 (0, 0,
                                                  0, 0,
                                                  4),
                                                 end_fn=end_fn)

    lib.aoc.give_answer(2023, 17, 2, answer)

INPUT = lib.aoc.get_input(2023, 17)
part1(INPUT)
part2(INPUT)
