import collections

import lib.aoc
import lib.ocr

def partition(nums, stride):
    assert(len(nums) % stride == 0)

    out = []

    for i in range(0, len(nums), stride):
        out.append(nums[i:i+stride])

    return out

WIDTH = 25
HEIGHT = 6
LAYER_LENGTH = WIDTH*HEIGHT

def part1(s):
    best = (LAYER_LENGTH, 0)

    for layer in partition(list(map(int, s)), LAYER_LENGTH):
        c = collections.Counter(layer)
        key = (c[0], c[1] * c[2])
        best = min(best, key)

    answer = best[1]

    print(f'The answer to part one is {answer}')

def part2(s):
    composite = [2] * LAYER_LENGTH

    for layer in partition(list(map(int, s)), LAYER_LENGTH):
        for i, (image_cell, layer_cell) in enumerate(zip(composite, layer)):
            if image_cell == 2:
                composite[i] = layer_cell

    assert(2 not in composite)

    image = partition(composite, WIDTH)

    white_cells = [(x, y)
                   for y, row in enumerate(image)
                   for x, cell in enumerate(row)
                   if cell == 1]

    answer = lib.ocr.parse_coord_set(white_cells)

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2019, 8)
part1(INPUT)
part2(INPUT)
