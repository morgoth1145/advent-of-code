import collections

import lib.aoc

def part1(s):
    coords = list(tuple(map(int, l.split(',')))
                  for l in s.splitlines())

    graph = collections.defaultdict(set)

    distances = []

    for i, (x, y, z) in enumerate(coords):
        for x2, y2, z2 in coords[i+1:]:
            d = ((x-x2)**2 + (y-y2)**2 + (z-z2)**2)
            distances.append((d, (x, y, z), (x2, y2, z2)))

    distances.sort()

    for d, (x, y, z), (x2, y2, z2) in distances[:1000]:
        graph[x,y,z].add((x2, y2, z2))
        graph[x2,y2,z2].add((x,y,z))

    circuits = []

    handled = set()

    def make_circuit(x, y, z, circuit):
        circuit.add((x, y, z))
        if (x, y, z) in handled:
            return
        handled.add((x, y, z))

        for x2, y2, z2 in graph[x,y,z]:
            make_circuit(x2, y2, z2, circuit)

    for x, y, z in coords:
        if (x, y, z) in handled:
            continue
        circuit = set()
        make_circuit(x, y, z, circuit)

        circuits.append(circuit)

    circuits.sort(key=lambda c: len(c))

    answer = len(circuits[-1]) * len(circuits[-2]) * len(circuits[-3])

    lib.aoc.give_answer(2025, 8, 1, answer)

def part2(s):
    coords = list(tuple(map(int, l.split(',')))
                  for l in s.splitlines())

    graph = collections.defaultdict(set)

    distances = []

    for i, (x, y, z) in enumerate(coords):
        for x2, y2, z2 in coords[i+1:]:
            d = ((x-x2)**2 + (y-y2)**2 + (z-z2)**2)
            distances.append((d, (x, y, z), (x2, y2, z2)))

    distances.sort()

    def check_fully_connected():
        handled = set()

        def make_circuit(x, y, z):
            if (x, y, z) in handled:
                return
            handled.add((x, y, z))

            for x2, y2, z2 in graph[x,y,z]:
                make_circuit(x2, y2, z2)

        make_circuit(*coords[0])
        return len(handled) == len(coords)

    for i, (d, (x, y, z), (x2, y2, z2)) in enumerate(distances):
        graph[x,y,z].add((x2, y2, z2))
        graph[x2,y2,z2].add((x,y,z))

        if check_fully_connected():
            answer = x*x2
            break

    lib.aoc.give_answer(2025, 8, 2, answer)

INPUT = lib.aoc.get_input(2025, 8)
part1(INPUT)
part2(INPUT)
