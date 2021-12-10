import lib.aoc

def score_line(line):
    seen = []
    for c in line:
        if c in '([{<':
            seen.append(c)
            continue
        if c not in ')]}>':
            assert(False)
        if 0 == len(seen):
            # These aren't supposed to have too many closers!
            assert(False)
        if c == ')':
            if seen[-1] == '(':
                seen = seen[:-1]
                continue
            return 3
        if c == ']':
            if seen[-1] == '[':
                seen = seen[:-1]
                continue
            return 57
        if c == '}':
            if seen[-1] == '{':
                seen = seen[:-1]
                continue
            return 1197
        if c == '>':
            if seen[-1] == '<':
                seen = seen[:-1]
                continue
            return 25137
    if len(seen):
        return None

    # These aren't supposed to be valid!
    assert(False)

def part1(s):
    answer = 0

    for line in s.splitlines():
        score = score_line(line)
        if score is not None:
            answer += score

    print(f'The answer to part one is {answer}')

def part2(s):
    pass

INPUT = lib.aoc.get_input(2021, 10)
part1(INPUT)
part2(INPUT)
