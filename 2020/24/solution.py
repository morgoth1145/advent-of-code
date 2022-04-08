import collections
import re

import lib.aoc
import lib.hex_coord

def get_initially_active_tiles(move_list):
    active_tiles = set()
    for moves in move_list.splitlines():
        pos = lib.hex_coord.EWHexCoord()
        for move in re.findall('e|w|se|sw|nw|ne', moves):
            pos = pos.move(move)
        if pos in active_tiles:
            active_tiles.remove(pos)
        else:
            active_tiles.add(pos)
    return active_tiles

def part1(s):
    answer = len(get_initially_active_tiles(s))
    lib.aoc.give_answer(2020, 24, 1, answer)

def iterate(active_tiles):
    neighbor_counts = collections.defaultdict(int)
    for pos in active_tiles:
        for n in pos.neighbors:
            neighbor_counts[n] += 1
    new_active = {pos
                  for pos in active_tiles
                  if neighbor_counts.pop(pos, 0) in (1, 2)}
    new_active |= {pos
                   for pos, count in neighbor_counts.items()
                   if count == 2}
    return new_active

def part2(s):
    active_tiles = get_initially_active_tiles(s)
    for _ in range(100):
        active_tiles = iterate(active_tiles)
    answer = len(active_tiles)
    lib.aoc.give_answer(2020, 24, 2, answer)

INPUT = lib.aoc.get_input(2020, 24)

part1(INPUT)
part2(INPUT)
