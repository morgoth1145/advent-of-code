import lib.aoc
import lib.graph
import lib.grid

def part1(s):
    grid = lib.grid.FixedGrid.parse(s)

    start = grid.find('S')
    end = grid.find('E')

    start_state = (start, (1, 0))

    def neighbor_fn(state):
        (x, y), (dx, dy) = state
        n = x+dx, y+dy
        if grid[n] != '#':
            yield (n, (dx, dy)), 1

        yield ((x, y), (-dy, dx)), 1000
        yield ((x, y), (dy, -dx)), 1000

    def end_fn(state):
        return state[0] == end

    graph = lib.graph.make_lazy_graph(neighbor_fn)

    answer = lib.graph.dijkstra_length_fuzzy_end(graph, start_state, end_fn)

    lib.aoc.give_answer(2024, 16, 1, answer)

def part2(s):
    grid = lib.grid.FixedGrid.parse(s)

    start = grid.find('S')
    end = grid.find('E')

    start_state = (start, (1, 0))

    def neighbor_fn(state):
        (x, y), (dx, dy) = state
        n = x+dx, y+dy
        if grid[n] != '#':
            yield (n, (dx, dy)), 1

        yield ((x, y), (-dy, dx)), 1000
        yield ((x, y), (dy, -dx)), 1000

    def end_fn(state):
        return state[0] == end

    graph = lib.graph.make_lazy_graph(neighbor_fn)

    best_dist = lib.graph.dijkstra_length_fuzzy_end(graph, start_state, end_fn)

    on_best_path = set()

    best_seen = {}
    known_retvals = {}

    def impl(state, cost):
        retval = known_retvals.get((state, cost))
        if retval is not None:
            return retval

        if cost > best_dist:
            known_retvals[state, cost] = False
            return False

        if best_seen.get(state, cost) < cost:
            known_retvals[state, cost] = False
            return False

        best_seen[state] = cost

        if end_fn(state):
            assert(cost == best_dist)
            on_best_path.add(state[0])
            known_retvals[state, cost] = True
            return True

        if cost == best_dist:
            known_retvals[state, cost] = False
            return False

        is_good = False

        for neighbor, n_cost in graph[state]:
            if impl(neighbor, cost+n_cost):
                on_best_path.add(state[0])
                is_good = True

        known_retvals[state, cost] = is_good
        return is_good

    impl(start_state, 0)

    answer = len(on_best_path)

    lib.aoc.give_answer(2024, 16, 2, answer)

INPUT = lib.aoc.get_input(2024, 16)
part1(INPUT)
part2(INPUT)
