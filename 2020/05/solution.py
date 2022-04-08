import lib.aoc

def iter_seats(s):
    for seat in s.splitlines():
        yield int(seat.translate(str.maketrans('FBLR', '0101')), 2)

def part1(s):
    answer = max(iter_seats(s))
    lib.aoc.give_answer(2020, 5, 1, answer)

def part2(s):
    seats = set(iter_seats(s))
    answer = [s for s in range(min(seats), max(seats)) if s not in seats][0]
    lib.aoc.give_answer(2020, 5, 2, answer)

INPUT = lib.aoc.get_input(2020, 5)
part1(INPUT)
part2(INPUT)
