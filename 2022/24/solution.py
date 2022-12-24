import functools

import lib.aoc
import lib.graph
import lib.grid

def part1(s):
    grid = lib.grid.FixedGrid.parse(s)

    blizzards = [(c, v) for c, v in grid.items()
                 if v not in '.#']

    start = min(x for x in range(grid.width) if grid[x,0] == '.'), 0
    end = min(x for x in range(grid.width) if grid[x,grid.height-1] == '.'), grid.height-1

    BLIZZARD_MOVEMENT = {
        '^': (0, -1),
        'v': (0, 1),
        '<': (-1, 0),
        '>': (1, 0),
    }

    @functools.cache
    def step_blizzards(blizzards):
        moved = []

        for (x, y), v in blizzards:
            dx, dy = BLIZZARD_MOVEMENT[v]
            x += dx
            y += dy
            if grid[x,y] == '#':
                x -= dx
                y -= dy
                while grid[x,y] != '#':
                    x -= dx
                    y -= dy
                x += dx
                y += dy
            moved.append(((x, y), v))

        return tuple(moved)

    def neighbor_fn(state):
        (x, y), blizzards = state
        new_blizzards = step_blizzards(blizzards)
        blizzard_squares = set(c for c,v in new_blizzards)

        for n in grid.neighbors(x, y):
            if grid[n] == '#':
                continue
            if n in blizzard_squares:
                continue
            yield (n, new_blizzards), 1

        if (x, y) not in blizzard_squares:
            yield ((x, y), new_blizzards), 1

    graph = lib.graph.make_lazy_graph(neighbor_fn)

    def end_fn(state):
        return state[0] == end

    def heuristic(state):
        (x, y), _ = state
        return abs(x-end[0]) + abs(y-end[1])

    answer = lib.graph.dijkstra_length_fuzzy_end(graph, (start, tuple(blizzards)),
                                                 end_fn, heuristic=heuristic)

    lib.aoc.give_answer(2022, 24, 1, answer)

def part2(s):
    pass

INPUT = lib.aoc.get_input(2022, 24)
part1(INPUT)
part2(INPUT)
