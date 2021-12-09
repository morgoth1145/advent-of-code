import lib.aoc

def parse(s):
    grid = []
    for line in s.splitlines():
        grid.append(list(map(int, line)))
    return grid

def part1(s):
    grid = parse(s)

    answer = 0

    for x, row in enumerate(grid):
        for y, val in enumerate(row):
            if x > 0:
                if grid[x-1][y] <= val:
                    continue
            if x < len(grid)-1:
                if grid[x+1][y] <= val:
                    continue
            if y > 0:
                if row[y-1] <= val:
                    continue
            if y < len(row)-1:
                if row[y+1] <= val:
                    continue
            answer += val+1

    print(f'The answer to part one is {answer}')

def part2(s):
    pass

INPUT = lib.aoc.get_input(2021, 9)
part1(INPUT)
part2(INPUT)
