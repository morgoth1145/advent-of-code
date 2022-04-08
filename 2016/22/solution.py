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
        x, y = int(m.group(1)), int(m.group(2))
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

    lib.aoc.give_answer(2016, 22, 1, answer)

def part2(s):
    nodes = parse_nodes(s)
    target = max((x, y)
                 for x, y in nodes.keys()
                 if y == 0)

    min_size, max_used = nodes[0, 0][0:2]

    xt, yt = target
    for x in range(xt):
        for y in [0, 1]:
            size, used, _, _ = nodes[x, y]
            min_size = min(min_size, size)
            max_used = max(max_used, used)

    assert(max_used <= min_size)

    # We can use standard sliding puzzle techniques!

    empty_positions = []
    for n, (_, used, _, _) in nodes.items():
        if used == 0:
            empty_positions.append(n)

    assert(len(empty_positions) == 1)
    # Assumption: We cannot ever gain a second empty cursor

    # Figure out how to move empty to the best sliding puzzle position to start

    target_to_slide = (xt-1, 0)

    steps = 0

    while target_to_slide not in empty_positions:
        steps += 1

        new_empty_positions = set()

        for x, y in empty_positions:
            size, _, _, _ = nodes[x, y]
            neighbors = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
            for n in neighbors:
                if n == target:
                    # Bad path
                    continue
                info = nodes.get(n)
                if info is None:
                    continue
                used = info[1]
                if used <= size:
                    new_empty_positions.add(n)

        empty_positions = new_empty_positions

    # We have the cursor in position!
    # We can just math the rest. It takes 5 steps per cycle (moving the target
    # left 1 and looping the empty tile around to the other side) and xt-1
    # cycles until the empty tile is at the 0, 0 node. One extra move puts our
    # payload where we want it to be!
    extra_steps = 5 * (xt - 1) + 1

    answer = steps + extra_steps

    lib.aoc.give_answer(2016, 22, 2, answer)

INPUT = lib.aoc.get_input(2016, 22)
part1(INPUT)
part2(INPUT)
