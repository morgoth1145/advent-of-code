import collections

import lib.aoc

def parse_input(s):
    bots = collections.defaultdict(list)
    instructions = collections.defaultdict(list)

    for line in s.splitlines():
        parts = line.split()
        if 'bot' == parts[0]:
            low_out = parts[5] == 'output'
            low_target = int(parts[6])
            high_out = parts[10] == 'output'
            high_target = int(parts[11])
            instructions[int(parts[1])].append((low_out, low_target,
                                                high_out, high_target))
        else:
            assert(parts[0] == 'value')
            val = int(parts[1])
            target = int(parts[5])
            bots[target].append(val)

    return bots, instructions

def part1(s):
    bots, instructions = parse_input(s)

    while True:
        for bot, values in bots.items():
            if len(values) == 2:
                break

        assert(len(values) == 2)
        low, high = min(values), max(values)
        if low == 17 and high == 61:
            answer = bot
            break

        del bots[bot]
        low_out, low_target, high_out, high_target = instructions[bot].pop(0)

        if not low_out:
            bots[low_target].append(low)
        if not high_out:
            bots[high_target].append(high)

    lib.aoc.give_answer(2016, 10, 1, answer)

def part2(s):
    bots, instructions = parse_input(s)
    outputs = {}

    while True:
        done = True
        for bot, values in bots.items():
            if len(values) == 2:
                done = False
                break

        if done:
            break

        low, high = min(values), max(values)

        del bots[bot]
        low_out, low_target, high_out, high_target = instructions[bot].pop(0)

        if low_out:
            outputs[low_target] = low
        else:
            bots[low_target].append(low)
        if high_out:
            outputs[high_target] = high
        else:
            bots[high_target].append(high)

    answer = outputs[0] * outputs[1] * outputs[2]

    lib.aoc.give_answer(2016, 10, 2, answer)

INPUT = lib.aoc.get_input(2016, 10)
part1(INPUT)
part2(INPUT)
