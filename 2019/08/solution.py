import collections

import lib.aoc

def parse_layers(s, width, height):
    nums = list(map(int, s))

    assert(len(nums) % (width * height) == 0)

    for i in range(0, len(nums), width * height):
        layer = nums[i:i+width*height]

        yield layer

def part1(s):
    best = (len(s), 0)

    for layer in parse_layers(s, 25, 6):
        c = collections.Counter(layer)
        key = (c[0], c[1] * c[2])
        best = min(best, key)

    answer = best[1]

    print(f'The answer to part one is {answer}')

def part2(s):
    pass

INPUT = lib.aoc.get_input(2019, 8)
part1(INPUT)
part2(INPUT)
