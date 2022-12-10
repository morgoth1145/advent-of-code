import lib.aoc

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
    pass

INPUT = lib.aoc.get_input(2022, 10)
part1(INPUT)
part2(INPUT)
