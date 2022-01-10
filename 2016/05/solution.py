import hashlib

import lib.aoc

def interesting_hashes(s):
    idx = 0
    while True:
        test = s + str(idx)
        h = hashlib.md5(test.encode()).hexdigest()
        if h[:5] == '00000':
            yield h
        idx += 1

def part1(s):
    answer = ''

    for h in interesting_hashes(s):
        answer += h[5]
        if len(answer) == 8:
            break

    print(f'The answer to part one is {answer}')

def part2(s):
    pass

INPUT = lib.aoc.get_input(2016, 5)
part1(INPUT)
part2(INPUT)
