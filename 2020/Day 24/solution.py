import collections

import helpers.input

def split_tile_moves(line):
    output = []
    while line:
        if line[0] in 'sn':
            output.append(line[:2])
            line = line[2:]
        else:
            output.append(line[0])
            line = line[1:]
    return output

def tile_neighbor(pos, move):
    x, y = pos
    if move == 'e':
        return x+1, y
    if move == 'w':
        return x-1, y
    if move == 'sw':
        return x-1, y-1
    if move == 'se':
        return x, y-1
    if move == 'nw':
        return x, y+1
    if move == 'ne':
        return x+1, y+1

def get_final_position(pos, moves):
    for m in moves:
        pos = tile_neighbor(pos, m)
    return pos

def part1(s):
    lines = s.splitlines()
    tiles = {}
    for l in lines:
        pos = get_final_position((0,0), split_tile_moves(l))
        tiles[pos] = not tiles.get(pos, False)
    answer = sum(1 for v in tiles.values() if v)
    print(f'The answer to part one is {answer}')

def part2(s):
    pass

INPUT = helpers.input.get_input(2020, 24)

part1(INPUT)
part2(INPUT)
