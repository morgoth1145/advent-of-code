import lib.aoc

def full_reduce(s):
    stack = []

    for unit in s:
        if stack:
            if stack[-1].swapcase() == unit:
                # Reaction
                stack.pop(-1)
                continue

        stack.append(unit)

    return ''.join(stack)

def part1(s):
    answer = len(full_reduce(s))

    print(f'The answer to part one is {answer}')

def part2(s):
    answer = len(s)

    for t in 'abcdefghijklmnopqrstuvwxyz':
        cand = full_reduce(s.replace(t, '').replace(t.upper(), ''))
        answer = min(answer, len(cand))

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2018, 5)
part1(INPUT)
part2(INPUT)
