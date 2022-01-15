import lib.aoc

def next_row(row):
    row = '.' + row + '.'

    next_row = []
    for left, center, right in zip(row, row[1:], row[2:]):
        if left + center + right in ('^^.',
                                     '.^^',
                                     '^..',
                                     '..^'):
            # Trap
            next_row.append('^')
        else:
            next_row.append('.')

    return ''.join(next_row)

def make_map(first_row, total_rows):
    rows = [first_row]
    last_row = first_row

    for _ in range(total_rows-1):
        last_row = next_row(last_row)
        rows.append(last_row)

    return '\n'.join(rows)

def part1(s):
    answer = make_map(s, 40).count('.')

    print(f'The answer to part one is {answer}')

def part2(s):
    answer = make_map(s, 400000).count('.')

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2016, 18)
part1(INPUT)
part2(INPUT)
