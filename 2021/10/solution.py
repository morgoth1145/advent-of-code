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
        return seen

    # These aren't supposed to be valid!
    assert(False)

def part1(s):
    answer = 0

    for line in s.splitlines():
        score = score_line(line)
        if score is not None and isinstance(score, int):
            answer += score

    print(f'The answer to part one is {answer}')

def autocomplete_score(to_finish):
    ratings = {
        '(': 1,
        '[': 2,
        '{': 3,
        '<': 4
    }
    score = 0
    for c in to_finish[::-1]:
        score = score * 5 + ratings[c]
    return score

def part2(s):
    incomplete_lines = []

    for line in s.splitlines():
        score = score_line(line)
        if isinstance(score, list):
            incomplete_lines.append((line, score))

    auto_scores = sorted(autocomplete_score(to_finish)
                         for line, to_finish in incomplete_lines)

    assert(len(auto_scores)%2 == 1)

    answer = auto_scores[len(auto_scores)//2]

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2021, 10)
part1(INPUT)
part2(INPUT)
