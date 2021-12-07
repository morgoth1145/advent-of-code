import os

year = int(input('Year: '))
day = int(input('Day: '))

path = f'{year}/{day:02}/solution.py'

os.makedirs(os.path.split(path)[0], exist_ok=True)

def part_1_template():
    return f'''def part1(s):
##    nums = list(map(lambda r:r[0], parse.findall('{{:d}}', s)))
##    lines = s.splitlines()
##    groups = s.split('\\n\\n')

    print(f'The answer to part one is {{answer}}')
    if input('Submit answer? ').lower() in ('y', 'yes', '1'):
        assert(lib.aoc.submit_answer({year}, {day}, 1, answer))'''

def part_2_template():
    if day == 25:
        return f'''def part2(s):
    print('There is no part two for Christmas!')
    lib.aoc.submit_answer({year}, 25, 2, 1)'''

    return f'''def part2(s):
    pass
##    print(f'The answer to part two is {{answer}}')
##    if input('Submit answer? ').lower() in ('y', 'yes', '1'):
##        assert(lib.aoc.submit_answer({year}, {day}, 2, answer))'''

template = f'''import collections
import functools
import itertools
import math
import parse
import re

import lib.aoc
import lib.graph
import lib.math
import lib.parsing

{part_1_template()}

{part_2_template()}

INPUT = lib.aoc.get_input({year}, {day})
part1(INPUT)
part2(INPUT)
'''

with open(path, 'w+') as f:
    f.write(template)

print(f'Template file created for {year}/{day}')
os.system('pause')
