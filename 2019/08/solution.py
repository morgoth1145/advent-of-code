import collections

import lib.aoc
import lib.ocr

def parse_layers(s, width, height):
    nums = list(map(int, s))

    assert(len(nums) % (width * height) == 0)

    for i in range(0, len(nums), width * height):
        layer_nums = nums[i:i+width*height]

        layer = []

        for j in range(0, width*height, width):
            layer.append(layer_nums[j:j+width])

        yield layer

def part1(s):
    best = (len(s), 0)

    for layer in parse_layers(s, 25, 6):
        c = collections.Counter()
        for row in layer:
            c += collections.Counter(row)
        key = (c[0], c[1] * c[2])
        best = min(best, key)

    answer = best[1]

    print(f'The answer to part one is {answer}')

def part2(s):
    image = [[2] * 25
             for _ in range(6)]

    for layer in parse_layers(s, 25, 6):
        for image_row, layer_row in zip(image, layer):
            for x, (image_cell, layer_cell) in enumerate(zip(image_row, layer_row)):
                if image_cell == 2:
                    image_row[x] = layer_cell

    white_cells = set()

    for y, row in enumerate(image):
        for x, cell in enumerate(row):
            assert(cell != 2)
            if cell == 1:
                white_cells.add((x, y))

    answer = lib.ocr.parse_coord_set(white_cells)

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2019, 8)
part1(INPUT)
part2(INPUT)
