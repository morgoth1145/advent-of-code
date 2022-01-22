import lib.aoc

def part1(s):
    answer = 'abcdefghijklmnop'

    for inst in s.split(','):
        if inst[0] == 's':
            x = int(inst[1:])
            answer = answer[-x:] + answer[:-x]
        elif inst[0] == 'x':
            a, b = sorted(map(int, inst[1:].split('/')))
            answer = answer[:a] + answer[b] + answer[a+1:b] + answer[a] + answer[b+1:]
        elif inst[0] == 'p':
            a = inst[1]
            assert(inst[2] == '/')
            b = inst[3]
            answer = answer.translate(str.maketrans(a+b, b+a))
        else:
            assert(False)

    print(f'The answer to part one is {answer}')

def part2(s):
    pass

INPUT = lib.aoc.get_input(2017, 16)
part1(INPUT)
part2(INPUT)
