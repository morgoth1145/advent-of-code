import collections
import math
import re

import helpers.input

def parse_tiles(s):
    tiles = {}
    for part in s.split('\n\n'):
        lines = part.splitlines()
        m = re.fullmatch('Tile (\d+):', lines[0])
        num = int(m.group(1))
        grid = [list(l) for l in lines[1:]]
        tiles[num] = grid
    return tiles

def determine_grid_borders(grid):
    top = grid[0]
    right = ''.join(l[-1] for l in grid)
    bottom = grid[-1]
    left = ''.join(l[0] for l in grid)
    return (top, right, bottom, left)

def grid_mirrors(grid):
    candidates = [grid]
    candidates.append(grid[::-1])
    candidates.append([l[::-1] for l in grid])
    candidates.append([l[::-1] for l in grid][::-1])
    return candidates

def grid_rotations(grid):
    candidates = [grid]
    last = grid
    for _ in range(3):
        grid = [l[:] for l in grid]
        for x in range(len(grid)):
            for y in range(len(grid[x])):
                grid[x][y] = last[len(grid[x])-y-1][x]
        last = grid
        candidates.append(grid)
    return candidates

def all_grid_options(grid):
    candidates = list()
    for opt in grid_mirrors(grid):
        candidates.extend(grid_rotations(opt))
    output = []
    for opt in candidates:
        if opt not in output:
            output.append(opt)
    return output

def generate_tiling(tile_to_orients_to_borders):
    dim = math.isqrt(len(tile_to_orients_to_borders))
    def impl(tiling, x, y, seen):
        if y == dim:
            return tiling
        next_x = x+1
        next_y = y
        if next_x == dim:
            next_x = 0
            next_y += 1
        for num, options in tile_to_orients_to_borders.items():
            if num in seen:
                continue
            seen.add(num)
            for idx, borders in options.items():
                top, _, _, left = borders
                if x > 0:
                    neighbor_num, neighbor_orient = tiling[x-1][y]
                    _, neighbor_right, _, _ = tile_to_orients_to_borders[neighbor_num][neighbor_orient]
                    if neighbor_right != left:
                        continue
                if y > 0:
                    neighbor_num, neighbor_orient = tiling[x][y-1]
                    _, _, neighbor_bottom, _ = tile_to_orients_to_borders[neighbor_num][neighbor_orient]
                    if neighbor_bottom != top:
                        continue
                tiling[x][y] = (num, idx)
                answer = impl(tiling, next_x, next_y, seen)
                if answer is not None:
                    return answer
            seen.remove(num)
        tiling[x][y] = None
        return None
    tiling = [[None] * dim for _ in range(dim)]
    return impl(tiling, 0, 0, set())

def part1(s):
    tiles = parse_tiles(s)
    tile_options = {num:all_grid_options(grid)
                    for num, grid in tiles.items()}
    tile_to_orients_to_borders = collections.defaultdict(dict)
    for num, options in tile_options.items():
        for idx, grid in enumerate(options):
            borders = determine_grid_borders(grid)
            tile_to_orients_to_borders[num][idx] = borders
    tiling = generate_tiling(tile_to_orients_to_borders)
    parts = [tiling[0][0], tiling[0][-1], tiling[-1][0], tiling[-1][-1]]
    answer = 1
    for p, _ in parts:
        answer *= p
    print(f'The answer to part one is {answer}')

def part2(s):
    pass

INPUT = helpers.input.get_input(2020, 20)

part1(INPUT)
part2(INPUT)
