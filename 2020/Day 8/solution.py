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

def run(instructions):
    acc = 0
    idx = 0
    previously_run = set()
    while True:
        if idx == len(instructions):
            return acc
        if idx in previously_run:
            return None
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

def part2(s):
    answer = None
    instructions = list(s.splitlines())
    for idx in range(len(instructions)):
        inst = instructions[idx]
        op, val = inst.split()
        if op == 'nop':
            instructions[idx] = f'jmp {val}'
            answer = run(instructions)
            instructions[idx] = inst
        elif op == 'jmp':
            instructions[idx] = f'nop {val}'
            answer = run(instructions)
            instructions[idx] = inst
        else:
            continue
        if answer is not None:
            break
    assert(answer is not None)
    print(f'The answer to part two is {answer}')

INPUT = helpers.input.get_input(2020, 8)

part1(INPUT)
part2(INPUT)
