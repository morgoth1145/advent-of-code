import helpers.input

def iter_seats(s):
    for seat in s.splitlines():
        row = seat[:7]
        column = seat[7:]
        row = row.replace('B', '1').replace('F', '0')
        column = column.replace('R', '1').replace('L', '0')
        yield int(row, 2), int(column, 2)

def part1(s):
    answer = 0
    for row, column in iter_seats(s):
        seat_id = row * 8 + column
        answer = max(seat_id, answer)
    print(f'The answer to part one is {answer}')

def part2(s):
    seen = set()
    for row, column in iter_seats(s):
        seat_id = row * 8 + column
        seen.add(seat_id)
    for i in range(1, 1<<10):
        if i in seen:
            continue
        if i-1 not in seen:
            continue
        if i+1 not in seen:
            continue
        answer = i
        break
    print(f'The answer to part two is {answer}')

INPUT = helpers.input.get_input(2020, 5)
part1(INPUT)
part2(INPUT)
