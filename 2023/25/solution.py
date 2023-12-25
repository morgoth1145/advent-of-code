import collections

import lib.aoc

def parse_input(s):
    m = collections.defaultdict(set)
    for line in s.splitlines():
        a, b = line.split(': ')
        for d in b.split():
            m[a].add(d)
            m[d].add(a)
    return m

def group_sizes(m, all_wires):
    sizes = []

    handled = set()

    todo = set(all_wires)

    while todo:
        start = list(todo)[0]

        group = set()

        queue = [start]

        while queue:
            n = queue.pop()
            if n in group:
                continue
            group.add(n)

            queue.extend(m.get(n, []))

        sizes.append(len(group))

        handled |= group

        todo -= group

    return sizes

def part1(s):
    m = parse_input(s)

    wires = set()
    all_nodes = set()

    for src, dests in m.items():
        for d in dests:
            a = min(src, d)
            b = max(src, d)
            wires.add((a, b))
            all_nodes.add(d)
        all_nodes.add(src)

##    # Output for daggity
##    for node in all_nodes:
##        print(node)
##
##    for src, dest in wires:
##        print(f'{src} -> {dest}')

    # Found via manual analysis with https://www.dagitty.net/dags.html
    to_rem = ['xhl', 'zgp', 'fxk']

    to_rem_wires = [(src, dest)
                    for src, dest in wires
                    if src in to_rem or dest in to_rem]

    answer = None

    for i, w in enumerate(to_rem_wires):
        s,d = w
        m[s].remove(d)
        m[d].remove(s)
        for i2, w2 in enumerate(to_rem_wires[i+1:], start=i+1):
            s2,d2 = w2
            m[s2].remove(d2)
            m[d2].remove(s2)
            for i3, w3 in enumerate(to_rem_wires[i2+1:], start=i2+1):

                s3,d3 = w3
                m[s3].remove(d3)
                m[d3].remove(s3)

                sizes = group_sizes(m, all_nodes)

                if len(sizes) == 2:
                    answer = sizes[0] * sizes[1]
                    break

                m[s3].add(d3)
                m[d3].add(s3)

            if answer is not None:
                break

            m[s2].add(d2)
            m[d2].add(s2)
        if answer is not None:
            break

        m[s].add(d)
        m[d].add(s)

    lib.aoc.give_answer(2023, 25, 1, answer)

def part2(s):
    print('There is no part two for Christmas!')

INPUT = lib.aoc.get_input(2023, 25)
part1(INPUT)
part2(INPUT)
