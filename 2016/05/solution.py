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
    answer = [None] * 8
    known = 0

    for h in interesting_hashes(s):
        pos = h[5]
        if pos not in '01234567':
            continue
        pos = int(pos)
        if answer[pos] is not None:
            continue
        answer[pos] = h[6]
        known += 1
        if known == 8:
            break

    answer = ''.join(answer)

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2016, 5)
part1(INPUT)
part2(INPUT)
