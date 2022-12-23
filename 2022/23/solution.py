import collections

import lib.aoc
import lib.grid

class Grove:
    def __init__(self, s):
        self.elves = {c for c,v in lib.grid.FixedGrid.parse(s).items()
                      if v == '#'}
        self.search_order = [
            [(-1, -1), (0, -1), (1, -1)], # North
            [(-1, 1), (0, 1), (1, 1)], # South
            [(-1, -1), (-1, 0), (-1, 1)], # West
            [(1, -1), (1, 0), (1, 1)], # East
        ]

    def step(self):
        targets = collections.defaultdict(list)

        for x, y in self.elves:
            if not any((tx, ty) in self.elves
                       for tx in (x-1, x, x+1)
                       for ty in (y-1, y, y+1)
                       if tx != x or ty != y):
                # No neighbor elves
                continue

            for search in self.search_order:
                if not any((x+dx, y+dy) in self.elves
                           for dx, dy in search):
                    dx, dy = search[1] # The target is the middle of the search
                    targets[x+dx, y+dy].append((x, y))
                    break

        self.search_order = self.search_order[1:] + self.search_order[:1]

        moves = 0

        for (tx, ty), elves in targets.items():
            if len(elves) > 1:
                continue
            self.elves.add((tx, ty))
            self.elves.remove(elves[0])
            moves += 1

        return moves > 0

def part1(s):
    grove = Grove(s)

    for _ in range(10):
        grove.step()

    min_x = min(x for x, y in grove.elves)
    max_x = max(x for x, y in grove.elves)

    min_y = min(y for x, y in grove.elves)
    max_y = max(y for x, y in grove.elves)

    answer = (max_x - min_x + 1) * (max_y - min_y + 1) - len(grove.elves)

    lib.aoc.give_answer(2022, 23, 1, answer)

def part2(s):
    grove = Grove(s)

    rounds_with_movement = 0
    while grove.step():
        rounds_with_movement += 1

    # First round *without* movement
    answer = rounds_with_movement + 1

    lib.aoc.give_answer(2022, 23, 2, answer)

INPUT = lib.aoc.get_input(2022, 23)
part1(INPUT)
part2(INPUT)
