import lib.aoc

def run_intcode(program):
    idx = 0

    def take_num():
        nonlocal idx
        val = program[idx]
        idx += 1
        return val

    def take_num_by_ref():
        nonlocal idx
        ref = program[idx]
        idx += 1
        return program[ref]

    while True:
        opcode = take_num()
        if opcode == 1:
            a = take_num_by_ref()
            b = take_num_by_ref()
            c = take_num()
            program[c] = a + b
            continue
        if opcode == 2:
            a = take_num_by_ref()
            b = take_num_by_ref()
            c = take_num()
            program[c] = a * b
            continue
        if opcode == 99:
            return
        assert(False)

def part1(s):
    program = list(map(int, s.split(',')))

    program[1] = 12
    program[2] = 2

    run_intcode(program)

    answer = program[0]

    print(f'The answer to part one is {answer}')

def part2(s):
    pass

INPUT = lib.aoc.get_input(2019, 2)
part1(INPUT)
part2(INPUT)
