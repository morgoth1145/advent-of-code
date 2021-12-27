import datetime
import os
import subprocess
import sys

import lib.aoc

def error_exit(msg):
    print(msg)
    os.system('pause')
    sys.exit(-1)

def open_editor(path):
    # Opens the IDLE editor for the path requested. This is done with a
    # separate command window so that when this program closes its command
    # window can cleanly disappear
    subprocess.Popen(['start', 'cmd', '/c', 'editor.bat', path],
                     shell=True)

def get_template(year, day):
    part_1_template = f'''def part1(s):
##    nums = list(map(lambda r:r[0], parse.findall('{{:d}}', s)))
##    lines = s.splitlines()
##    groups = s.split('\\n\\n')
##    grid = lib.grid.FixedGrid.parse(s, value_fn=int)
##    grid = lib.grid.FixedGrid.parse(s,
##                                    linesplit_fn=lambda line: line.split(),
##                                    value_fn=int)

    print(f'The answer to part one is {{answer}}')
    if input('Submit answer? ').lower() in ('y', 'yes', '1'):
        assert(lib.aoc.submit_answer({year}, {day}, 1, answer))'''

    if day == 25:
        part_2_template = f'''def part2(s):
    print('There is no part two for Christmas!')'''
    else:
        part_2_template = f'''def part2(s):
    pass
##    print(f'The answer to part two is {{answer}}')
##    if input('Submit answer? ').lower() in ('y', 'yes', '1'):
##        assert(lib.aoc.submit_answer({year}, {day}, 2, answer))'''

    return f'''import collections
import functools
import itertools
import math
import parse
import re

import lib.aoc
import lib.graph
from lib.graphics import *
import lib.grid
import lib.math
import lib.ocr
import lib.parsing

{part_1_template}

{part_2_template}

INPUT = lib.aoc.get_input({year}, {day})
part1(INPUT)
part2(INPUT)
'''

year = int(input('Year: '))

if year < 2015:
    error_exit(f'Advent of Code started in 2015! Year {year} is invalid')

day = int(input('Day: '))

if day not in range(1, 26):
    error_exit(f'Advent of code runs from December 1st through 25th. Day {day} is invalid')

time_to_release = lib.aoc.time_to_release(year, day)
if time_to_release >= datetime.timedelta(days=1):
    error_exit(f'{year} Day {day} is more than a day in the future!')

path = f'{year}/{day:02}/solution.py'

if not os.path.exists(path):
    print(f'Writing template for {year} Day {day}')
    os.makedirs(os.path.split(path)[0], exist_ok=True)
    with open(path, 'w+') as f:
        f.write(get_template(year, day))

open_editor(path)

if time_to_release <= datetime.timedelta(days=-1):
    print(f'{year} Day {day} is more than a day in the past!')
    if input('Begin time trial? ').lower() in ('y', 'yes', '1'):
        lib.aoc.begin_time_trial(year, day)
else:
    lib.aoc.download_input_when_live(year, day)
