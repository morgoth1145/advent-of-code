import collections

import lib.aoc

def parse_input(s):
    dep_graph = collections.defaultdict(set)
    all_steps = set()

    for line in s.splitlines():
        _, a, _, _, _, _, _, b, _, _ = line.split()
        dep_graph[b].add(a)
        all_steps.add(b)
        all_steps.add(a)

    return dep_graph, all_steps

def part1(s):
    dep_graph, all_steps = parse_input(s)

    todo = sorted(all_steps)

    done = set()
    order = []

    while len(order) < len(todo):
        for step in todo:
            if step in done:
                continue
            if len(dep_graph[step] - done) == 0:
                # We can do this now!
                order.append(step)
                done.add(step)
                break

    answer = ''.join(order)

    print(f'The answer to part one is {answer}')

def part2(s):
    pass

INPUT = lib.aoc.get_input(2018, 7)
part1(INPUT)
part2(INPUT)
