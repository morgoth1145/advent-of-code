import lib.aoc

def part1(s):
    steps = int(s)
    buffer = [0]

    pos = 0

    for n in range(1, 2018):
        pos = (pos + steps) % len(buffer)
        buffer.insert(pos+1, n)
        pos += 1

    answer = buffer[(buffer.index(2017)+1) % len(buffer)]

    print(f'The answer to part one is {answer}')

def part2(s):
    pass

INPUT = lib.aoc.get_input(2017, 17)
part1(INPUT)
part2(INPUT)
