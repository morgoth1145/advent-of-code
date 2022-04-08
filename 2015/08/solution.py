import lib.aoc

def decoded_savings(line):
    assert(line[0] == '"' == line[-1])

    saved = 2
    line = line[1:-1]

    idx = 0
    while idx < len(line):
        if line[idx] == '\\':
            if line[idx+1] == 'x':
                idx += 4
                saved += 3
                continue
            else:
                idx += 2
                saved += 1
                continue

        idx += 1

    return saved

def part1(s):
    answer = sum(map(decoded_savings, s.splitlines()))

    lib.aoc.give_answer(2015, 8, 1, answer)

def part2(s):
    answer = sum(2 + line.count('"') + line.count('\\')
                 for line in s.splitlines())

    lib.aoc.give_answer(2015, 8, 2, answer)

INPUT = lib.aoc.get_input(2015, 8)
part1(INPUT)
part2(INPUT)
