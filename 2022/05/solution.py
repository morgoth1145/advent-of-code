import parse

import lib.aoc

def parse_input(s):
    a, b = s.split('\n\n')

    lines = a.splitlines()

    stacks = [[] for _ in range(len(lines.pop().split()))]

    while lines:
        row = lines.pop()
        for i in range(len(stacks)):
            entry = row[4*i+1]
            if entry != ' ':
                stacks[i].append(entry)

    moves = list(parse.findall('move {:d} from {:d} to {:d}', b))

    return stacks, moves

def part1(s):
    stacks, moves = parse_input(s)

    for n, source, target in moves:
        # zero index
        source -= 1
        target -= 1

        for _ in range(n):
            stacks[target].append(stacks[source].pop(-1))

    answer = ''
    for s in stacks:
        answer += s[-1]

    lib.aoc.give_answer(2022, 5, 1, answer)

def part2(s):
    stacks, moves = parse_input(s)

    for n, source, target in moves:
        # zero index
        source -= 1
        target -= 1

        moved = stacks[source][-n:]
        stacks[source] = stacks[source][:-n]
        stacks[target] += moved

    answer = ''
    for s in stacks:
        answer += s[-1]

    lib.aoc.give_answer(2022, 5, 2, answer)

INPUT = lib.aoc.get_input(2022, 5)
part1(INPUT)
part2(INPUT)
