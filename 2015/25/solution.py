import lib.aoc

def part1(s):
    line = s.split()
    row = int(line[15][:-1])
    col = int(line[17][:-1])

    idx = col
    last_finished_col = col + row - 1
    idx += last_finished_col * (last_finished_col-1) // 2

    MOD = 33554393

    answer = (20151125 * pow(252533, idx-1, MOD)) % MOD

    lib.aoc.give_answer(2015, 25, 1, answer)

def part2(s):
    print('There is no part two for Christmas!')

INPUT = lib.aoc.get_input(2015, 25)
part1(INPUT)
part2(INPUT)
