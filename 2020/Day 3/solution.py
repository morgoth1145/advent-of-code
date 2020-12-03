import helpers.input

def part1(s):
    answer = 0
    x = 0
    for line in s.splitlines():
        if line[x] == '#':
            answer += 1
        x = (x + 3) % len(line)
    print(f'The answer to part one is {answer}')

def part2(s):
    pass

INPUT = helpers.input.get_input(2020, 3)
part1(INPUT)
part2(INPUT)
