import re

import lib.aoc

def parse_nodes(s):
    nodes = {}
    for line in s.splitlines()[2:]:
        p, size, used, avail, perc = line.split()
        m = re.match('/dev/grid/node\-x(\d+)\-y(\d+)', p)
        assert(size[-1] == 'T')
        assert(used[-1] == 'T')
        assert(avail[-1] == 'T')
        size = int(size[:-1])
        used = int(used[:-1])
        avail = int(avail[:-1])
        x, y = m.group(1), m.group(2)
        nodes[x,y] = (size, used, avail, perc)
    return nodes

def part1(s):
    nodes = parse_nodes(s)

    answer = 0

    for a, (_, useda, _, _) in nodes.items():
        if useda == 0:
            continue
        for b, (_, _, availb, _) in nodes.items():
            if a == b:
                continue
            if availb >= useda:
                answer += 1

    print(f'The answer to part one is {answer}')

def part2(s):
    pass

INPUT = lib.aoc.get_input(2016, 22)
part1(INPUT)
part2(INPUT)
