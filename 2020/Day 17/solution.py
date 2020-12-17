import collections

import helpers.input

def iter_neighbors(coord):
    x, y, z = coord
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            for dz in (-1, 0, 1):
                if dx == dy == dz == 0:
                    continue
                yield (x+dx, y+dy, z+dz)

def do_cycle(prev_active):
    active_counts = collections.defaultdict(int)
    for coord in prev_active:
        for neighbor in iter_neighbors(coord):
            active_counts[neighbor] += 1
    new_active = []
    for coord in prev_active:
        count = active_counts.pop(coord, 0)
        if count in (2, 3):
            new_active.append(coord)
    for coord, count in active_counts.items():
        if count == 3:
            new_active.append(coord)
    return new_active

def part1(s):
    active_coords = []
    for y, line in enumerate(s.splitlines()):
        for x, c in enumerate(line):
            if c == '#':
                active_coords.append((x, y, 0))
    for _ in range(6):
        active_coords = do_cycle(active_coords)
    answer = len(active_coords)
    print(f'The answer to part one is {answer}')

def iter_neighbors2(coord):
    x, y, z, w = coord
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            for dz in (-1, 0, 1):
                for dw in (-1, 0, 1):
                    if dx == dy == dz == dw == 0:
                        continue
                    yield (x+dx, y+dy, z+dz, w+dw)

def do_cycle2(prev_active):
    active_counts = collections.defaultdict(int)
    for coord in prev_active:
        for neighbor in iter_neighbors2(coord):
            active_counts[neighbor] += 1
    new_active = []
    for coord in prev_active:
        count = active_counts.pop(coord, 0)
        if count in (2, 3):
            new_active.append(coord)
    for coord, count in active_counts.items():
        if count == 3:
            new_active.append(coord)
    return new_active

def part2(s):
    active_coords = []
    for y, line in enumerate(s.splitlines()):
        for x, c in enumerate(line):
            if c == '#':
                active_coords.append((x, y, 0, 0))
    for _ in range(6):
        active_coords = do_cycle2(active_coords)
    answer = len(active_coords)
    print(f'The answer to part two is {answer}')

INPUT = helpers.input.get_input(2020, 17)

part1(INPUT)
part2(INPUT)
