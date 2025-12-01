import lib.aoc

def solve(s, dial_size, dial_start, per_click):
    answer = 0

    pos = dial_start

    for line in s.splitlines():
        if line[0] == 'R':
            d = 1
        elif line[0] == 'L':
            d = -1
        else:
            assert(False)
        n = int(line[1:])

        if per_click:
            for _ in range(n):
                pos = (pos + d) % dial_size
                if pos == 0:
                    answer += 1
        else:
            pos = (pos + d*n) % dial_size
            if pos == 0:
                answer += 1

    return answer

def part1(s):
    answer = solve(s, 100, 50, per_click=False)

    lib.aoc.give_answer(2025, 1, 1, answer)

def part2(s):
    answer = solve(s, 100, 50, per_click=True)

    lib.aoc.give_answer(2025, 1, 2, answer)

INPUT = lib.aoc.get_input(2025, 1)
part1(INPUT)
part2(INPUT)
