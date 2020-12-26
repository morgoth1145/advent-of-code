import helpers.input

def iter_seats(s):
    for seat in s.splitlines():
        yield int(seat.translate(str.maketrans('FBLR', '0101')), 2)

def part1(s):
    answer = max(iter_seats(s))
    print(f'The answer to part one is {answer}')

def part2(s):
    seats = set(iter_seats(s))
    answer = [s for s in range(min(seats), max(seats)) if s not in seats][0]
    print(f'The answer to part two is {answer}')

INPUT = helpers.input.get_input(2020, 5)
part1(INPUT)
part2(INPUT)
