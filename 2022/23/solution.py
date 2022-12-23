import collections

import lib.aoc
import lib.grid

def iterate(grid, times):
    def test_north(targets, x, y):
        if all((test_x, y-1) not in grid or grid[test_x, y-1] == '.'
               for test_x in (x-1, x, x+1)):
            targets[x, y-1].append(c)
            return True

        return False

    def test_south(targets, x, y):
        if all((test_x, y+1) not in grid or grid[test_x, y+1] == '.'
               for test_x in (x-1, x, x+1)):
            targets[x, y+1].append(c)
            return True

        return False

    def test_west(targets, x, y):
        if all((x-1, test_y) not in grid or grid[x-1, test_y] == '.'
               for test_y in (y-1, y, y+1)):
            targets[x-1, y].append(c)
            return True

        return False

    def test_east(targets, x, y):
        if all((x+1, test_y) not in grid or grid[x+1, test_y] == '.'
               for test_y in (y-1, y, y+1)):
            targets[x+1, y].append(c)
            return True

        return False

    search_order = [test_north, test_south, test_west, test_east]

    def neighbors(x, y):
        for tx in (x-1, x, x+1):
            for ty in (y-1, y, y+1):
                if tx == x and ty == y:
                    continue
                yield tx, ty

    for i in range(times):
        targets = collections.defaultdict(list)

        for c, v in grid.items():
            x, y = c

            if v == '.':
                continue
            if all(grid.get(n, '.') == '.'
                   for n in neighbors(x, y)):
                continue

            for test in search_order:
                if test(targets, x, y):
                    break

        search_order = search_order[1:] + search_order[:1]

        for target, elves in targets.items():
            if len(elves) > 1:
                continue
            elf = elves[0]
            grid[target] = '#'
            grid[elf] = '.'

def part1(s):
    grid = lib.grid.FixedGrid.parse(s).to_dict()

    iterate(grid, 10)

    min_x = min(x for (x, y), v in grid.items() if v == '#')
    max_x = max(x for (x, y), v in grid.items() if v == '#')
    x_range = range(min_x, max_x+1)

    min_y = min(y for (x, y), v in grid.items() if v == '#')
    max_y = max(y for (x, y), v in grid.items() if v == '#')
    y_range = range(min_y, max_y+1)

    answer = sum(1
                 for x in x_range
                 for y in y_range
                 if grid.get((x,y), '.') == '.')

    lib.aoc.give_answer(2022, 23, 1, answer)

def part2(s):
    pass

INPUT = lib.aoc.get_input(2022, 23)
part1(INPUT)
part2(INPUT)
