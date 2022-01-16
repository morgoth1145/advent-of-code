import heapq

import lib.aoc
import lib.graph
import lib.grid

def get_point_of_interest_graph(s):
    grid = lib.grid.FixedGrid.parse(s)

    poi_graph = {}

    for start, v in grid.items():
        if v not in '#.':
            destinations = []

            def neighbor_fn(pos):
                if pos != start and grid[pos] != '.':
                    return
                for n in grid.neighbors(*pos):
                    nv = grid[n]
                    if nv == '#':
                        continue
                    yield n, 1

            for pos, dist in lib.graph.all_reachable(lib.graph.make_lazy_graph(neighbor_fn),
                                                     start):
                if grid[pos] == '.':
                    continue
                destinations.append((int(grid[pos]), dist))

            poi_graph[int(v)] = destinations

    return poi_graph

def part1(s):
    graph = get_point_of_interest_graph(s)

    all_points_of_interest = tuple(sorted(graph.keys()))

    queue = [(0, 0, (0,))]
    handled = set()

    while True:
        current_dist, pos, seen = heapq.heappop(queue)

        if seen == all_points_of_interest:
            answer = current_dist
            break

        if (pos, seen) in handled:
            continue

        handled.add((pos, seen))

        for neighbor, dist in graph[pos]:
            new_seen = tuple(sorted(set(seen + (neighbor,))))
            heapq.heappush(queue, (current_dist + dist, neighbor, new_seen))

    print(f'The answer to part one is {answer}')

def part2(s):
    graph = get_point_of_interest_graph(s)

    all_points_of_interest = tuple(sorted(graph.keys()))

    queue = [(0, 0, (0,))]
    handled = set()

    while True:
        current_dist, pos, seen = heapq.heappop(queue)

        if seen == all_points_of_interest and pos == 0:
            answer = current_dist
            break

        if (pos, seen) in handled:
            continue

        handled.add((pos, seen))

        for neighbor, dist in graph[pos]:
            new_seen = tuple(sorted(set(seen + (neighbor,))))
            heapq.heappush(queue, (current_dist + dist, neighbor, new_seen))

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2016, 24)
part1(INPUT)
part2(INPUT)
