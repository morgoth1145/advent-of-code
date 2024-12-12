import lib.aoc
import lib.grid

class Region:
    def __init__(self, grid, start_cell):
        self.cells = set()
        target = grid[start_cell]

        to_handle = [start_cell]
        seen = set(to_handle)

        while to_handle:
            c = to_handle.pop()
            self.cells.add(c)
            for n in grid.neighbors(*c):
                if n in seen or grid[n] != target:
                    continue
                seen.add(n)
                to_handle.append(n)

    @property
    def area(self):
        return len(self.cells)

    @property
    def perimeter(self):
        perimeter = 0

        for x, y in self.cells:
            for n in [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]:
                if n not in self.cells:
                    perimeter += 1

        return perimeter

    @property
    def num_sides(self):
        num_sides = 0

        # Count similarly to counting the perimeter, but only include the
        # "rightmost" edge on any given side. This ensures that each side
        # will only be counted once!
        for x, y in self.cells:
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                if (x+dx, y+dy) not in self.cells:
                    # This is part of the perimeter, now check if it's a "key"
                    # section for counting sides
                    rdx, rdy = -dy, dx
                    if ((x+rdx, y+rdy) in self.cells and
                        (x+dx+rdx, y+dy+rdy) not in self.cells):
                        # Not a key section, don't count it
                        continue
                    num_sides += 1

        return num_sides

def solve(s, region_scorer):
    grid = lib.grid.FixedGrid.parse(s)

    answer = 0
    handled = set()

    for coord, c in grid.items():
        if coord in handled:
            continue
        r = Region(grid, coord)
        handled.update(r.cells)
        answer += region_scorer(r)

    return answer

def part1(s):
    answer = solve(s, lambda r: r.area * r.perimeter)

    lib.aoc.give_answer(2024, 12, 1, answer)

def part2(s):
    answer = solve(s, lambda r: r.area * r.num_sides)

    lib.aoc.give_answer(2024, 12, 2, answer)

INPUT = lib.aoc.get_input(2024, 12)
part1(INPUT)
part2(INPUT)
