import lib.aoc

def part1(s):
    answer = sum(map(int, s.splitlines()))

    print(f'The answer to part one is {answer}')

def part2(s):
    changes = list(map(int, s.splitlines()))

    f = 0
    seen = set()

    while True:
        done = False

        for d in changes:
            f += d
            if f in seen:
                done = True
                break
            seen.add(f)

        if done:
            break

    answer = f

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2018, 1)
part1(INPUT)
part2(INPUT)
