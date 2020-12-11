import helpers.input

def advance(prev):
    grid = [l[:] for l in prev]
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == '.':
                continue
            occupied = 0
            candidates = [(i-1,j-1),
                          (i-1,j),
                          (i-1,j+1),
                          (i,j-1),
                          (i,j+1),
                          (i+1,j-1),
                          (i+1,j),
                          (i+1,j+1)]
            for x, y in candidates:
                if x < 0 or x >= len(grid) or y < 0 or y >= len(grid[x]):
                    continue
                if prev[x][y] == '#':
                    occupied += 1
            if grid[i][j] == 'L':
                if occupied == 0:
                    grid[i][j] = '#'
            else:
                if occupied >= 4:
                    grid[i][j] = 'L'
    return grid

def part1(s):
    grid = list(map(list, s.splitlines()))
    while True:
        new_grid = advance(grid)
        if new_grid == grid:
            break
        grid = new_grid
    answer = ''.join(''.join(l) for l in grid).count('#')
    print(f'The answer to part one is {answer}')

def advance2(prev):
    grid = [l[:] for l in prev]
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == '.':
                continue
            occupied = 0
            candidates = [(-1, -1),
                          (-1, 0),
                          (-1, +1),
                          ( 0, -1),
                          ( 0, +1),
                          (+1, -1),
                          (+1, 0),
                          (+1, +1)]
            for dx, dy in candidates:
                x, y = i, j
                while True:
                    x += dx
                    y += dy
                    if x < 0 or x >= len(grid) or y < 0 or y >= len(grid[x]):
                        break
                    if prev[x][y] == '.':
                        continue
                    if prev[x][y] == '#':
                        occupied += 1
                    break
            if grid[i][j] == 'L':
                if occupied == 0:
                    grid[i][j] = '#'
            else: # Occupied
                if occupied >= 5:
                    grid[i][j] = 'L'
    return grid

def part2(s):
    grid = list(map(list, s.splitlines()))
    while True:
        new_grid = advance2(grid)
        if new_grid == grid:
            break
        grid = new_grid
    answer = ''.join(''.join(l) for l in grid).count('#')
    print(f'The answer to part two is {answer}')

INPUT = helpers.input.get_input(2020, 11)

part1(INPUT)
part2(INPUT)