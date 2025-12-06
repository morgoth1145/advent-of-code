import math

import lib.aoc
import lib.grid

def part1(s):
    grid = lib.grid.FixedGrid.parse(s,
                                    linesplit_fn=lambda line: line.split(),
                                    value_fn=str)

    answer = 0

    for x in grid.x_range:
        col = grid.col(x)

        op = col[-1]

        nums = list(map(int, col[:-1]))

        if op == '+':
            answer += sum(nums)
        elif op == '*':
            answer += math.prod(nums)
        else:
            assert(False)

    lib.aoc.give_answer(2025, 6, 1, answer)

def part2(s):
    lines = s.splitlines()

    split_indices = []

    for i in range(len(lines[0])):
        if all(l[i] == ' ' for l in lines):
            split_indices.append(i)

    def split_line(line):
        out = []
        start = 0
        for i in split_indices:
            out.append(line[start:i])
            start = i+1
        out.append(line[start:])
        return out

    grid = lib.grid.FixedGrid.parse(s,
                                    linesplit_fn=lambda line: split_line(line),
                                    value_fn=str)

    answer = 0

    for x in grid.x_range:
        col = grid.col(x)

        op = col[-1].strip()

        pre_nums = col[:-1]

        nums2 = []

        i = 0
        while True:
            out = ''

            for n in pre_nums:
                if i >= len(n) or n[i] == ' ':
                    continue
                out += n[i]

            if out == '':
                break

            nums2.append(out)
            i += 1

        nums = list(map(int, nums2))

        if op == '+':
            answer += sum(nums)
        elif op == '*':
            answer += math.prod(nums)
        else:
            assert(False)

    lib.aoc.give_answer(2025, 6, 2, answer)

INPUT = lib.aoc.get_input(2025, 6)
part1(INPUT)
part2(INPUT)
