import lib.aoc

def solve(s):
    assert(s[0] == '{' and s[-1] == '}')

    score = 0
    depth = 0

    ignoring = False
    garbage = False
    discarded = 0

    for c in s:
        if ignoring:
            assert(garbage)
            ignoring = False
            continue
        if garbage:
            if c == '>':
                garbage = False
                continue
            if c == '!':
                ignoring = True
                continue
            discarded += 1
            continue
        if c == '<':
            garbage = True
            continue
        if c == ',':
            continue
        if c == '{':
            depth += 1
            continue
        if c == '}':
            score += depth
            depth -= 1
            continue
        assert(False)

    assert(depth == 0)

    return score, discarded

def part1(s):
    answer, _ = solve(s)

    print(f'The answer to part one is {answer}')

def part2(s):
    _, answer = solve(s)

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2017, 9)
part1(INPUT)
part2(INPUT)
