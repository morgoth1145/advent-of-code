import lib.aoc
import lib.ocr

def parse_input(s):
    for line in s.splitlines():
        inst = line.split()
        if len(inst) > 1:
            inst[1] = int(inst[1])
        yield inst

def part1(s):
    strengths_per_cycle = []

    x = 1
    for inst in parse_input(s):
        strengths_per_cycle.append(x * len(strengths_per_cycle) + x)
        if inst[0] == 'noop':
            continue
        if inst[0] == 'addx':
            # Takes two cycles
            strengths_per_cycle.append(x * len(strengths_per_cycle) + x)
            x += inst[1]
            continue
        assert(False)

    answer = strengths_per_cycle[19] + strengths_per_cycle[59] + strengths_per_cycle[99] + strengths_per_cycle[139] + strengths_per_cycle[179] + strengths_per_cycle[219]

    lib.aoc.give_answer(2022, 10, 1, answer)

def part2(s):
    pos_per_cycle = []

    x = 1
    for inst in parse_input(s):
        pos_per_cycle.append(x)
        if inst[0] == 'noop':
            continue
        if inst[0] == 'addx':
            # Takes two cycles
            pos_per_cycle.append(x)
            x += inst[1]
            continue
        assert(False)

    lit_pixels = set()

    for x, pos in enumerate(pos_per_cycle):
        y = x // 40
        if x % 40 in (pos-1, pos, pos+1):
            lit_pixels.add((x%40, y))

    answer = lib.ocr.parse_coord_set(lit_pixels)

    lib.aoc.give_answer(2022, 10, 2, answer)

INPUT = lib.aoc.get_input(2022, 10)
part1(INPUT)
part2(INPUT)
