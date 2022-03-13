import lib.aoc

def react(s):
    for idx, (a, b) in enumerate(zip(s, s[1:])):
        if a == b:
            continue
        if a.lower() != b.lower():
            continue
        # Reaction
        return s[:idx] + s[idx+2:]
    return s

def part1(s):
    while True:
        reduced = react(s)
        if reduced == s:
            break
        s = reduced

    answer = len(s)

    print(f'The answer to part one is {answer}')

def part2(s):
    pass

INPUT = lib.aoc.get_input(2018, 5)
part1(INPUT)
part2(INPUT)
