import lib.aoc

def step(s):
    a = s
    b = s[::-1].translate(str.maketrans('01', '10'))
    return a + '0' + b

def checksum(s):
    if len(s) % 2 == 1:
        return s

    out = []

    for a, b in zip(s[::2], s[1::2]):
        if a == b:
            out.append('1')
        else:
            out.append('0')

    return checksum(''.join(out))

def part1(s):
    while len(s) < 272:
        s = step(s)

    s = s[:272]

    answer = checksum(s)

    print(f'The answer to part one is {answer}')

def part2(s):
    pass

INPUT = lib.aoc.get_input(2016, 16)
part1(INPUT)
part2(INPUT)
