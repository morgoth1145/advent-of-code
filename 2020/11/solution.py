import lib.aoc

def compute_immediate_neighbors(grid):
    grid_neighbors = [l[:] for l in grid]
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == '.':
                grid_neighbors[i][j] = None
                continue
            neighbors = []
            for dx in (-1, 0, 1):
                x = i+dx
                if x not in range(0, len(grid)):
                    continue
                for dy in (-1, 0, 1):
                    if dx == dy == 0:
                        continue
                    y = j+dy
                    if y not in range(0, len(grid[x])):
                        continue
                    if grid[x][y] == '.':
                        continue
                    neighbors.append((x, y))
            grid_neighbors[i][j] = tuple(neighbors)
    return grid_neighbors

def advance(prev, neighbors, occupied_evacuation_limit):
    grid = [l[:] for l in prev]
    for i, row in enumerate(grid):
        for j, c in enumerate(row):
            if c == '.':
                continue
            seats = [prev[x][y] for x,y in neighbors[i][j]]
            if c == 'L':
                if '#' not in seats:
                    grid[i][j] = '#'
            else:
                if seats.count('#') >= occupied_evacuation_limit:
                    grid[i][j] = 'L'
    return grid

def part1(s):
    grid = list(map(list, s.splitlines()))
    neighbors = compute_immediate_neighbors(grid)
    while True:
        new_grid = advance(grid, neighbors, 4)
        if new_grid == grid:
            break
        grid = new_grid
    answer = ''.join(''.join(l) for l in grid).count('#')
    print(f'The answer to part one is {answer}')

def compute_seen_neighbors(grid):
    grid_neighbors = [l[:] for l in grid]
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == '.':
                grid_neighbors[i][j] = None
                continue
            neighbors = []
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    if dx == dy == 0:
                        continue
                    x, y = i, j
                    while True:
                        x += dx
                        y += dy
                        if x not in range(0, len(grid)):
                            break
                        if y not in range(0, len(grid[x])):
                            break
                        if grid[x][y] == '.':
                            continue
                        neighbors.append((x, y))
                        break
            grid_neighbors[i][j] = neighbors
    return grid_neighbors

def part2(s):
    grid = list(map(list, s.splitlines()))
    neighbors = compute_seen_neighbors(grid)
    while True:
        new_grid = advance(grid, neighbors, 5)
        if new_grid == grid:
            break
        grid = new_grid
    answer = ''.join(''.join(l) for l in grid).count('#')
    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2020, 11)

part1(INPUT)
part2(INPUT)
