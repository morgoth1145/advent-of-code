import json
import parse

import lib.aoc

def part1(s):
    answer = sum(map(lambda r:r[0], parse.findall('{:d}', s)))

    print(f'The answer to part one is {answer}')

def sum_not_red(data):
    if isinstance(data, list):
        return sum(map(sum_not_red, data))
    if isinstance(data, int):
        return data
    if isinstance(data, str):
        return 0
    assert(isinstance(data, dict))
    if 'red' in data or 'red' in data.values():
        return 0

    return sum(map(sum_not_red, data.values()))

def part2(s):
    answer = sum_not_red(json.loads(s))

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2015, 12)
part1(INPUT)
part2(INPUT)
