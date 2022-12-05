import parse

import lib.aoc

def solve(s, move_handler):
    stacks, moves = s.split('\n\n')

    stack_lines = stacks.splitlines()

    stacks = [[] for _ in range(len(stack_lines.pop().split()))]

    for row in stack_lines[::-1]:
        for i, entry in enumerate(row[1::4]):
            if entry != ' ':
                stacks[i].append(entry)

    for n, source, target in parse.findall('move {:d} from {:d} to {:d}', moves):
        move_handler(stacks, n, source-1, target-1)

    return ''.join(s[-1] for s in stacks)

def part1(s):
    def move_blocks(stacks, n, source, target):
        for _ in range(n):
            stacks[target].append(stacks[source].pop(-1))

    answer = solve(s, move_blocks)

    lib.aoc.give_answer(2022, 5, 1, answer)

def part2(s):
    def move_blocks(stacks, n, source, target):
        moved = stacks[source][-n:]
        stacks[source] = stacks[source][:-n]
        stacks[target] += moved

    answer = solve(s, move_blocks)

    lib.aoc.give_answer(2022, 5, 2, answer)

INPUT = lib.aoc.get_input(2022, 5)
part1(INPUT)
part2(INPUT)
