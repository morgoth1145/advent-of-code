import helpers.input

def crack(subject_num, target):
    val = 1
    loop_size = 0
    while True:
        if val == target:
            return loop_size
        val *= subject_num
        val = val % 20201227
        loop_size += 1

def do_thing(subject_num, loop_size):
    val = 1
    for _ in range(loop_size):
        val *= subject_num
        val = val % 20201227
    return val

def part1(s):
    a, b = map(int, s.splitlines())
    loop_a = crack(7, a)
    answer = do_thing(b, loop_a)
    print(f'The answer to part one is {answer}')

def part2(s):
    print('There is no part two for Christmas!')

INPUT = helpers.input.get_input(2020, 25)

part1(INPUT)
part2(INPUT)
