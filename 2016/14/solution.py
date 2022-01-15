import hashlib

import lib.aoc

def gen_hashes(s):
    idx = 0
    while True:
        idx += 1
        h = hashlib.md5((s + str(idx)).encode()).hexdigest()
        yield h

def gen_keys(s):
    hashes = gen_hashes(s)

    window = []

    for _ in range(1000):
        window.append(next(hashes))

    idx = 0
    while True:
        idx += 1
        h = window.pop(0)
        window.append(next(hashes))

        triple = None
        for j in range(len(h)-2):
            if h[j] == h[j+1] == h[j+2]:
                triple = h[j]
                break

        if triple is None:
            continue

        target = triple * 5
        if any(target in test_h
               for test_h in window):
            yield h, idx

def part1(s):
    keys = gen_keys(s)

    for _ in range(64):
        _, answer = next(keys)

    print(f'The answer to part one is {answer}')

def part2(s):
    pass

INPUT = lib.aoc.get_input(2016, 14)
part1(INPUT)
part2(INPUT)
