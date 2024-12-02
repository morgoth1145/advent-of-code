import lib.aoc

def parse_reports(s):
    for report in s.splitlines():
        yield tuple(map(int, report.split()))

def validate(report):
    sign = 1 if report[1] > report[0] else -1
    for l0, l1 in zip(report, report[1:]):
        if not 1 <= (l1 - l0) * sign <= 3:
            return False
    return True

def part1(s):
    answer = sum(map(validate, parse_reports(s)))

    lib.aoc.give_answer(2024, 2, 1, answer)

def validate_tolerant(report):
    return validate(report) or any(validate(report[:i] + report[i+1:])
                                   for i in range(len(report)))

def part2(s):
    answer = sum(map(validate_tolerant, parse_reports(s)))

    lib.aoc.give_answer(2024, 2, 2, answer)

INPUT = lib.aoc.get_input(2024, 2)
part1(INPUT)
part2(INPUT)
