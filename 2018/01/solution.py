import lib.aoc

def part1(s):
    answer = sum(map(int, s.splitlines()))

    lib.aoc.give_answer(2018, 1, 1, answer)

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

    lib.aoc.give_answer(2018, 1, 2, answer)

INPUT = lib.aoc.get_input(2018, 1)
part1(INPUT)
part2(INPUT)
