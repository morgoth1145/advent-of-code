import helpers.input

def part1(s):
    instructions = list(s.splitlines())

    acc = 0
    idx = 0
    previously_run = set()
    while True:
        if idx in previously_run:
            break
        previously_run.add(idx)
        op, val = instructions[idx].split()
        val = int(val)
        if op == 'acc':
            acc = acc + val
            idx += 1
            continue
        if op == 'jmp':
            idx += val
            continue
        if op == 'nop':
            idx += 1
            continue
    answer = acc
    print(f'The answer to part one is {answer}')

def part2(s):
    pass

INPUT = helpers.input.get_input(2020, 8)

part1(INPUT)
part2(INPUT)
