import functools

import lib.aoc
import lib.graph
import lib.lazy_dict

def parse_cave(s):
    depth, target = s.splitlines()
    depth = int(depth.split()[1])
    tx, ty = target.split()[1].split(',')
    tx, ty = int(tx), int(ty)

    MOD = 20183

    @functools.cache
    def erosion_level(x, y):
        if (x, y) in [(0, 0), (tx, ty)]:
            return 0
        if y == 0:
            return (x * 16807 + depth) % MOD
        if x == 0:
            return (y * 48271 + depth) % MOD
        return (erosion_level(x-1, y) * erosion_level(x, y-1) + depth) % MOD

    def risk_level(coord):
        x, y = coord
        return erosion_level(x, y) % 3

    return lib.lazy_dict.make_lazy_dict(risk_level), tx, ty

def part1(s):
    cave, tx, ty = parse_cave(s)

    answer = sum(cave[x, y]
                 for x in range(tx+1)
                 for y in range(ty+1))

    print(f'The answer to part one is {answer}')

TORCH = 0
CLIMBING = 1
NEITHER = 2

VALID_TOOLS = {
    0: (TORCH, CLIMBING), # Rocky
    1: (CLIMBING, NEITHER), # Wet
    2: (TORCH, NEITHER), # Narrow
}

def part2(s):
    cave, tx, ty = parse_cave(s)

    def neighbor_fn(state):
        x, y, tool = state
        this_risk = cave[x,y]

        for other_tool in VALID_TOOLS[this_risk]:
            if tool != other_tool:
                yield (x, y, other_tool), 7

        for nx, ny in [(x-1, y),
                       (x+1, y),
                       (x, y+1),
                       (x, y-1)]:
            if nx < 0 or ny < 0:
                continue
            if tool not in VALID_TOOLS[cave[nx, ny]]:
                continue
            yield (nx, ny, tool), 1

    graph = lib.graph.make_lazy_graph(neighbor_fn)

    answer = lib.graph.dijkstra_length(graph,
                                       (0, 0, TORCH),
                                       (tx, ty, TORCH))

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2018, 22)
part1(INPUT)
part2(INPUT)
