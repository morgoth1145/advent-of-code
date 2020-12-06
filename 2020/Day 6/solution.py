import helpers.input

def part1(s):
    groups = s.split('\n\n')
    answer = 0
    for g in groups:
        g = ''.join(g.split())
        answer += len(set(g))
    print(f'The answer to part one is {answer}')

def part2(s):
    pass

INPUT = helpers.input.get_input(2020, 6)
part1(INPUT)
part2(INPUT)
