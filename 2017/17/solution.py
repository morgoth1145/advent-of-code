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
    steps = int(s)

    pos = 0
    length = 1
    target_pos = 0
    answer = None

    for n in range(1, 50000001):
        pos = (pos + steps) % length
        pos += 1 # Insert location
        if pos == target_pos:
            target_pos += 1
        elif pos == target_pos + 1:
            answer = n
        length += 1

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2017, 17)
part1(INPUT)
part2(INPUT)
