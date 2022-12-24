import lib.aoc
import lib.grid

class Valley:
    def __init__(self, s):
        grid = lib.grid.FixedGrid.parse(s)

        self.start = min(x for x in range(grid.width)
                         if grid[x,0] == '.'), 0
        self.goal = end = min(x for x in range(grid.width)
                              if grid[x, grid.height-1] == '.'), grid.height-1

        self.walls = {c for c, v in grid.items()
                      if v == '#'}
        # Don't let the elf escape the valley!
        self.walls.add((self.start[0], -1))
        self.walls.add((self.goal[0], grid.height))

        # Precompute all the blizzard states. However, precompute them on a
        # per-axis basis as those periods are much lower than the full period.

        blizzards = [(c, v) for c, v in grid.items()
                     if v in '^v']

        self.vertical_blizzards = []
        for _ in range(25): # Exclude wall tiles in the period!
            self.vertical_blizzards.append({c
                                            for c, v
                                            in blizzards})
            new_blizzards = []
            for (x, y), v in blizzards:
                y += 1 if v == 'v' else -1
                if y == 0:
                    y = grid.height-2
                elif y == grid.height-1:
                    y = 1
                new_blizzards.append(((x, y), v))
            blizzards = new_blizzards

        blizzards = [(c, v) for c, v in grid.items()
                     if v in '<>']

        self.horizontal_blizzards = []
        for _ in range(grid.width-2): # Exclude wall tiles in the period!
            self.horizontal_blizzards.append({c
                                              for c, v
                                              in blizzards})
            new_blizzards = []
            for (x, y), v in blizzards:
                x += 1 if v == '>' else -1
                if x == 0:
                    x = grid.width-2
                elif x == grid.width-1:
                    x = 1
                new_blizzards.append(((x, y), v))
            blizzards = new_blizzards

        self.step = 0

    def move_optimally(self, begin, target):
        states = {begin}

        while target not in states:
            self.step += 1

            blocked = set(self.walls)
            blocked |= self.vertical_blizzards[self.step % len(self.vertical_blizzards)]
            blocked |= self.horizontal_blizzards[self.step % len(self.horizontal_blizzards)]

            new_states = set()

            for x, y in states:
                for n in [(x-1, y),
                          (x+1, y),
                          (x, y-1),
                          (x, y+1)]:
                    if n in blocked:
                        continue
                    new_states.add(n)
                if (x, y) not in blocked:
                    new_states.add((x, y))

            states = new_states

def part1(s):
    valley = Valley(s)

    valley.move_optimally(valley.start, valley.goal)

    answer = valley.step

    lib.aoc.give_answer(2022, 24, 1, answer)

def part2(s):
    valley = Valley(s)

    # We don't need one giant search, we can just do each phase individually!
    valley.move_optimally(valley.start, valley.goal)
    valley.move_optimally(valley.goal, valley.start)
    valley.move_optimally(valley.start, valley.goal)

    answer = valley.step

    lib.aoc.give_answer(2022, 24, 2, answer)

INPUT = lib.aoc.get_input(2022, 24)
part1(INPUT)
part2(INPUT)
