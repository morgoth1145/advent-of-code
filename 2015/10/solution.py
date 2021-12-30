import lib.aoc

def expand(n):
    out = []

    last = None
    count = 0

    for c in n:
        if last != c:
            if last is not None:
                out.append(count)
                out.append(last)
            last = c
            count = 1
            continue

        count += 1

    out.append(count)
    out.append(last)

    return out

def part1(s):
    n = list(map(int, s))

    for _ in range(40):
        n = expand(n)

    answer = len(n)

    print(f'The answer to part one is {answer}')

def part2(s):
    pass

INPUT = lib.aoc.get_input(2015, 10)
part1(INPUT)
part2(INPUT)
