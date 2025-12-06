import math

import lib.aoc
import lib.grid

def solve(s, vertical_numbers=False):
    lines = s.splitlines()
    num_section = '\n'.join(lines[:-1])
    op_line = lines[-1]

    if vertical_numbers:
        # Pivot the table for easier parsing
        grid = lib.grid.FixedGrid.parse(num_section).transpose()
        num_columns_str = grid.as_str(line_spacing='').replace(' ', '')
        num_columns = [list(map(int, col.splitlines()))
                       for col in num_columns_str.split('\n\n')]
    else:
        grid = lib.grid.FixedGrid.parse(num_section,
                                        linesplit_fn=str.split,
                                        value_fn=int)
        num_columns = [grid.col(x) for x in grid.x_range]

    answer = 0

    for nums, op in zip(num_columns, op_line.split()):
        if op == '+':
            answer += sum(nums)
        elif op == '*':
            answer += math.prod(nums)
        else:
            assert(False)

    return answer

def part1(s):
    answer = solve(s)

    lib.aoc.give_answer(2025, 6, 1, answer)

def part2(s):
    answer = solve(s, vertical_numbers=True)

    lib.aoc.give_answer(2025, 6, 2, answer)

INPUT = lib.aoc.get_input(2025, 6)
part1(INPUT)
part2(INPUT)
