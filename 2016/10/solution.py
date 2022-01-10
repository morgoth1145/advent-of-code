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

    print(f'The answer to part one is {answer}')

def part2(s):
    pass

INPUT = lib.aoc.get_input(2016, 10)
part1(INPUT)
part2(INPUT)
