import lib.aoc

def parse_input(s):
    for line in s.splitlines():
        yield list(map(int, line.split()))

def extrapolate(line):
    stack = [line]
    while set(stack[-1]) != {0}:
        l = stack[-1]
        d = [v1-v0 for v0, v1 in zip(l, l[1:])]
        stack.append(d)

    stack[-1].append(0)

    while len(stack) > 1:
        l = stack.pop(-1)
        d = l[-1]
        stack[-1].append(stack[-1][-1] + d)

    return stack[0][-1]

def part1(s):
    data = list(parse_input(s))

    answer = sum(map(extrapolate, data))

    lib.aoc.give_answer(2023, 9, 1, answer)

def part2(s):
    pass

INPUT = lib.aoc.get_input(2023, 9)
part1(INPUT)
part2(INPUT)
