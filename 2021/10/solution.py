import lib.aoc

OPENINGS = '([{<'
CLOSINGS = ')]}>'
INVALID_SCORES = [3, 57, 1197, 25137]

def validate_line(line):
    seen = []
    for c in line:
        if c in OPENINGS:
            seen.append(c)
            continue
        close_idx = CLOSINGS.index(c)
        if seen[-1] == OPENINGS[close_idx]:
            seen.pop(-1)
            continue
        return INVALID_SCORES[close_idx], seen

    assert(len(seen)) # We shouldn't have any valid lines
    return None, seen

def part1(s):
    answer = sum(score
                 for score, _ in map(validate_line, s.splitlines())
                 if score is not None)

    print(f'The answer to part one is {answer}')

def autocomplete_score(to_finish):
    score = 0
    for c in to_finish[::-1]:
        # Each closing score is actually its index plus 1
        score = score * 5 + OPENINGS.index(c) + 1
    return score

def part2(s):
    auto_scores = sorted(autocomplete_score(to_finish)
                         for score, to_finish in map(validate_line,
                                                     s.splitlines())
                         if score is None)

    assert(len(auto_scores)%2 == 1)

    answer = auto_scores[len(auto_scores)//2]

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2021, 10)
part1(INPUT)
part2(INPUT)
