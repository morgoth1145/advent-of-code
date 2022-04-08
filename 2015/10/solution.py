import lib.aoc

def look_and_say(s, iterations):
    n = list(map(int, s))

    for _ in range(iterations):
        out = []

        last = None
        count = 0

        for c in n:
            if last != c:
                if last is not None:
                    out += [count, last]
                last, count = c, 1
                continue

            count += 1

        out += [count, last]

        n = out

    return len(n)

def part1(s):
    answer = look_and_say(s, 40)

    lib.aoc.give_answer(2015, 10, 1, answer)

def part2(s):
    answer = look_and_say(s, 50)

    lib.aoc.give_answer(2015, 10, 2, answer)

INPUT = lib.aoc.get_input(2015, 10)
part1(INPUT)
part2(INPUT)
