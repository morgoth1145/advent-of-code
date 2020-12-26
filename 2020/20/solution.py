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

def get_grid_borders(grid):
    top = ''.join(grid[0])
    right = ''.join(l[-1] for l in grid)
    bottom = ''.join(grid[-1])
    left = ''.join(l[0] for l in grid)
    return (top, right, bottom, left)

def canonical_border(border):
    # Since borders can be reversed due to symmetries, choose the 'smaller' one
    # as the canonical one for lookups
    return min(border, border[::-1])

def get_border_to_tiles_mapping(tiles):
    mapping = collections.defaultdict(set)
    for num, grid in tiles.items():
        for border in get_grid_borders(grid):
            mapping[canonical_border(border)].add(num)
    return mapping

def part1(s):
    tiles = parse_tiles(s)
    border_to_tiles = get_border_to_tiles_mapping(tiles)

    answer = 1
    for num, grid in tiles.items():
        shared_borders = 0
        for border in get_grid_borders(grid):
            if len(border_to_tiles[canonical_border(border)]) > 1:
                shared_borders += 1
        if shared_borders == 2:
            # It's a corner!
            answer *= num
    print(f'The answer to part one is {answer}')

def generate_grid_symmetries(grid):
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
    return candidates

def choose_tile(tiles, border_to_tiles, tiling, x, y, unused_tiles):
    candidates = set(unused_tiles)
    if x > 0:
        _, left_neighbor, _, _ = get_grid_borders(tiling[(x-1, y)])
        candidates &= border_to_tiles[canonical_border(left_neighbor)]
    else:
        left_neighbor = None
    if y > 0:
        _, _, top_neighbor, _ = get_grid_borders(tiling[(x, y-1)])
        candidates &= border_to_tiles[canonical_border(top_neighbor)]
    else:
        top_neighbor = None
    for num in candidates:
        for orientation in generate_grid_symmetries(tiles[num]):
            top, _, _, left = get_grid_borders(orientation)
            if left_neighbor is not None:
                if left_neighbor != left:
                    # This tile's border doesn't match its neighbor!
                    continue
            else:
                if len(border_to_tiles[canonical_border(left)]) > 1:
                    # This tile should have no possible left neighbor!
                    continue
            if top_neighbor is not None:
                if top_neighbor != top:
                    # This tile's border doesn't match its neighbor!
                    continue
            else:
                if len(border_to_tiles[canonical_border(top)]) > 1:
                    # This tile should have no possible upper neighbor!
                    continue
            return num, orientation
    assert(False)

def generate_tiling(tiles):
    border_to_tiles = get_border_to_tiles_mapping(tiles)

    unused_tiles = set(tiles.keys())

    dim = math.isqrt(len(tiles))
    tiling = {}
    for x in range(dim):
        for y in range(dim):
            num, tile = choose_tile(tiles,
                                    border_to_tiles,
                                    tiling,
                                    x, y,
                                    unused_tiles)
            unused_tiles.remove(num)
            tiling[(x, y)] = tile
    return dim, tiling

def generate_image(tiles):
    dim, tiling = generate_tiling(tiles)

    image = []
    for y in range(dim):
        row = [tiling[(x, y)] for x in range(dim)]
        # Chop off borders
        row = [[l[1:-1] for l in grid[1:-1]]
               for grid in row]
        for tile_y in range(len(row[0])):
            image.append([c
                          for grid in row
                          for c in grid[tile_y]])
    return image

def get_monster_tiles(image):
    MONSTER_PATTERN = '''                  # 
#    ##    ##    ###
 #  #  #  #  #  #   '''
    monster_coords = [(dx, dy)
                      for dy, line in enumerate(MONSTER_PATTERN.splitlines())
                      for dx, c in enumerate(line)
                      if c == '#']
    max_x = max(x for x,y in monster_coords)
    max_y = max(y for x,y in monster_coords)

    for y in range(len(image) - max_y):
        for x in range(len(image[y]) - max_x):
            if all(image[y+dy][x+dx] == '#'
                   for dx,dy in monster_coords):
                yield from ((x+dx, y+dy)
                            for dx,dy in monster_coords)

def count_non_monster_tiles(image):
    # Try all image symmetries
    for image in generate_grid_symmetries(image):
        monster_tiles = set(get_monster_tiles(image))
        if len(monster_tiles) == 0:
            continue
        all_pounds = {(x, y)
                      for y, row in enumerate(image)
                      for x, c in enumerate(row)
                      if c == '#'}
        return len(all_pounds - monster_tiles)
    assert(False)

def part2(s):
    answer = count_non_monster_tiles(generate_image(parse_tiles(s)))
    print(f'The answer to part two is {answer}')

INPUT = helpers.input.get_input(2020, 20)

part1(INPUT)
part2(INPUT)
