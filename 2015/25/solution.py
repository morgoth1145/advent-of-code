import lib.aoc

def parse_input(s):
    line = s.split()
    row = int(line[15][:-1])
    col = int(line[17][:-1])
    return row, col

def gen_codes():
    val = 20151125

    row, col = 1, 1

    while True:
        yield row, col, val

        val = (val * 252533) % 33554393
        if row > 1:
            row -= 1
            col += 1
        else:
            row, col = col+1, 1

def part1(s):
    target_row, target_col = parse_input(s)

    for row, col, val in gen_codes():
        if row == target_row and col == target_col:
            answer = val
            break

    print(f'The answer to part one is {answer}')

def part2(s):
    print('There is no part two for Christmas!')

INPUT = lib.aoc.get_input(2015, 25)
part1(INPUT)
part2(INPUT)
