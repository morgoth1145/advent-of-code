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

    START_STATE = (start, 0, tuple(blizzards))
    GOAL_1_PHASE = 0
    RETURN_PHASE = 1
    GOAL_2_PHASE = 2

    def neighbor_fn(state):
        (x, y), phase, blizzards = state
        new_blizzards = step_blizzards(blizzards)
        blizzard_squares = set(c for c,v in new_blizzards)

        for n in grid.neighbors(x, y):
            if grid[n] == '#':
                continue
            if n in blizzard_squares:
                continue
            if phase == GOAL_1_PHASE and n == end:
                yield (n, RETURN_PHASE, new_blizzards), 1
            elif phase == RETURN_PHASE and n == start:
                yield (n, GOAL_2_PHASE, new_blizzards), 1
            else:
                yield (n, phase, new_blizzards), 1

        if (x, y) not in blizzard_squares:
            yield ((x, y), phase, new_blizzards), 1

    graph = lib.graph.make_lazy_graph(neighbor_fn)

    def end_fn(state):
        return state[0] == end and state[1] == GOAL_2_PHASE

    START_TO_GOAL_DIST = sum(abs(s-e) for s,e in zip(start, end))

    def heuristic(state):
        (x, y), phase, _ = state
        if phase == GOAL_2_PHASE:
            return abs(x-end[0]) + abs(y-end[1])
        if phase == RETURN_PHASE:
            return abs(x-start[0]) + abs(y-start[1]) + START_TO_GOAL_DIST
        if phase == GOAL_1_PHASE:
            return abs(x-end[0]) + abs(y-end[1]) + 2 * START_TO_GOAL_DIST
        assert(False)

    answer = lib.graph.dijkstra_length_fuzzy_end(graph, START_STATE,
                                                 end_fn, heuristic=heuristic)

    lib.aoc.give_answer(2022, 24, 2, answer)

INPUT = lib.aoc.get_input(2022, 24)
part1(INPUT)
part2(INPUT)
