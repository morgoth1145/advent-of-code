import helpers.input

def iter_seats(s):
    for seat in s.splitlines():
        seat = seat.replace('B', '1').replace('R', '1')
        seat = seat.replace('F', '0').replace('L', '0')
        yield int(seat, 2)

def part1(s):
    answer = max(iter_seats(s))
    print(f'The answer to part one is {answer}')

def part2(s):
    seats = set(iter_seats(s))
    sub_1 = {seat_id-1 for seat_id in seats}
    plus_1 = {seat_id+1 for seat_id in seats}
    answer = list(sub_1.intersection(plus_1) - seats)[0]
    print(f'The answer to part two is {answer}')

INPUT = helpers.input.get_input(2020, 5)
part1(INPUT)
part2(INPUT)
