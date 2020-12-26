import collections
import itertools

import lib.aoc

def neighbor_coords(coord):
    neighbors = itertools.product(*((c-1, c, c+1)
                                    for c in coord))
    return (n for n in neighbors if n != coord)

def step(prev_active):
    active_counts = collections.defaultdict(int)
    for coord in prev_active:
        for neighbor in neighbor_coords(coord):
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

def parse_active_coords(s, coord_suffix):
    return active_coords

def run_simulation(s, dims, steps):
    active_coords = []
    for y, line in enumerate(s.splitlines()):
        for x, c in enumerate(line):
            if c == '#':
                active_coords.append((x, y) + (0,) * (dims - 2))
    for _ in range(steps):
        active_coords = step(active_coords)
    return len(active_coords)

def part1(s):
    answer = run_simulation(s, dims=3, steps=6)
    print(f'The answer to part one is {answer}')

def part2(s):
    answer = run_simulation(s, dims=4, steps=6)
    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2020, 17)

part1(INPUT)
part2(INPUT)
