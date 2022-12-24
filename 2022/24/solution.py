import lib.aoc
import lib.grid

class Valley:
    def __init__(self, s):
        grid = lib.grid.FixedGrid.parse(s)

        BLIZZARD_MOVEMENT = {
            '^': (0, -1),
            'v': (0, 1),
            '<': (-1, 0),
            '>': (1, 0),
        }

        self.blizzards = [(c, BLIZZARD_MOVEMENT[v]) for c, v in grid.items()
                          if v not in '.#']
        self.walls = {c for c, v in grid.items()
                      if v == '#'}
        self.start = min(x for x in range(grid.width)
                         if grid[x,0] == '.'), 0
        self.goal = end = min(x for x in range(grid.width)
                              if grid[x, grid.height-1] == '.'), grid.height-1
        # Don't let the elf escape the valley!
        self.walls.add((self.start[0], -1))
        self.walls.add((self.goal[0], grid.height))

    def move_optimally(self, begin, target):
        steps = 0
        states = {begin}

        while target not in states:
            steps += 1

            new_blizzards = []
            blizzard_squares = set()

            for (x, y), (dx, dy) in self.blizzards:
                x += dx
                y += dy
                if (x, y) in self.walls:
                    x -= dx
                    y -= dy
                    while (x, y) not in self.walls:
                        x -= dx
                        y -= dy
                    x += dx
                    y += dy
                new_blizzards.append(((x, y), (dx, dy)))
                blizzard_squares.add((x, y))

            self.blizzards = new_blizzards

            new_states = set()

            for x, y in states:
                for n in [(x-1, y),
                          (x+1, y),
                          (x, y-1),
                          (x, y+1)]:
                    if n in self.walls or n in blizzard_squares:
                        continue
                    new_states.add(n)
                if (x, y) not in self.walls and (x, y) not in blizzard_squares:
                    new_states.add((x, y))

            states = new_states

        return steps

def part1(s):
    valley = Valley(s)

    answer = valley.move_optimally(valley.start, valley.goal)

    lib.aoc.give_answer(2022, 24, 1, answer)

def part2(s):
    valley = Valley(s)

    # We don't need one giant search, we can just do each phase individually!
    answer = 0
    answer += valley.move_optimally(valley.start, valley.goal)
    answer += valley.move_optimally(valley.goal, valley.start)
    answer += valley.move_optimally(valley.start, valley.goal)

    lib.aoc.give_answer(2022, 24, 2, answer)

INPUT = lib.aoc.get_input(2022, 24)
part1(INPUT)
part2(INPUT)
