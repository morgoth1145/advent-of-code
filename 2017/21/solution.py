import lib.aoc

# Stolen from 2020 day 20
def get_all_symmetries(pattern):
    grid = [list(line) for line in pattern.split('/')]

    candidates = []

    # Generate all rotations
    for _ in range(4):
        last, grid = grid, [l[:] for l in grid]

        for x in range(len(last)):
            for y in range(len(last[x])):
                grid[x][y] = last[len(grid[x])-y-1][x]

        # Append both the grid and its vertical mirror to the candidate list
        # Other mirrorings will be generated automatically by the 4 rotations
        candidates.append(grid)
        candidates.append(grid[::-1])

    candidates = ['/'.join(''.join(line) for line in grid)
                  for grid in candidates]

    return sorted(set(candidates))

def solve(s, iterations):
    transforms = {}

    for line in s.splitlines():
        before, after = line.split(' => ')
        for before in get_all_symmetries(before):
            transforms[before] = after

    grid = ['.#.',
             '..#',
             '###']

    for _ in range(iterations):
        if len(grid) % 2 == 0:
            run = 2
        else:
            run = 3

        next_grid = []

        for y in range(0, len(grid), run):
            row_chunks = []
            for x in range(0, len(grid), run):
                block = '/'.join(grid[y+off][x:x+run]
                                 for off in range(run))

                row_chunks.append(transforms[block].split('/'))

            while row_chunks[0]:
                row = ''
                for chunk in row_chunks:
                    row += chunk.pop(0)
                next_grid.append(row)

        grid = next_grid

    return '/'.join(grid).count('#')

def part1(s):
    answer = solve(s, 5)

    print(f'The answer to part one is {answer}')

def part2(s):
    pass

INPUT = lib.aoc.get_input(2017, 21)
part1(INPUT)
part2(INPUT)
