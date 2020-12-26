import lib.aoc

def run(program, return_accumulator_on_looping=False):
    acc = 0
    idx = 0
    seen = set()
    while True:
        if idx == len(program):
            return acc
        if idx in seen:
            if return_accumulator_on_looping:
                return acc
            return None
        seen.add(idx)
        op, val = program[idx].split()
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
        assert(False)

def part1(s):
    program = list(s.splitlines())
    answer = run(program, True)
    print(f'The answer to part one is {answer}')

def part2(s):
    program = list(s.splitlines())
    for idx, inst in enumerate(program):
        if inst.startswith('nop'):
            program[idx] = inst.replace('nop', 'jmp')
            answer = run(program)
            program[idx] = inst
        elif inst.startswith('jmp'):
            program[idx] = inst.replace('jmp', 'nop')
            answer = run(program)
            program[idx] = inst
        else:
            continue
        if answer is not None:
            break
    assert(answer is not None)
    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2020, 8)

part1(INPUT)
part2(INPUT)
