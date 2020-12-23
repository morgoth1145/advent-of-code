import helpers.input

def move(cups):
    picked = cups[1:4]
    cups[1:4] = []
    dest = cups[0]-1
    if dest < min(cups):
        dest = max(cups)
    while dest in picked:
        dest -= 1
        if dest < min(cups):
            dest = max(cups)
    idx = cups.index(dest)
    cups[:idx+1] = cups[:idx+1] + picked
    cups = cups[1:] + cups[:1]
    return cups

def part1(s):
    cups = list(map(int, s))
    for _ in range(100):
        cups = move(cups[:])
    idx = cups.index(1)
    order = cups[idx+1:] + cups[:idx]
    answer = ''.join(map(str, order))
    print(f'The answer to part one is {answer}')

def part2(s):
    pass

INPUT = helpers.input.get_input(2020, 23)

part1(INPUT)
part2(INPUT)
