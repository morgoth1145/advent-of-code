import functools

import lib.aoc

def parse_input(s):
    for line in s.splitlines():
        a, b = line.split()
        yield a, list(map(int, b.split(',')))

@functools.cache
def gen_options(size, splits):
    def gen(rem_len, rem_splits):
        if len(rem_splits) == 0:
            yield '.' * rem_len
            return

        a = rem_splits[0]
        rest = rem_splits[1:]
        after = sum(rest) + len(rest)

        for before in range(rem_len-after-a+1):
            cand = '.' * before + '#' * a + '.'
            for opt in gen(rem_len-a-before-1, rest):
                yield cand + opt

    return list(gen(size, splits))

def find_matches(pattern, splits):
    options = gen_options(len(pattern), tuple(splits))

    for o in options:
        if all((c0==c1 or c0=='?')
               for c0,c1 in zip(pattern, o)):
            yield o

def part1(s):
    data = list(parse_input(s))

    answer = 0

    for a, b in data:
        answer += len(list(find_matches(a, b)))

    lib.aoc.give_answer(2023, 12, 1, answer)

def part2(s):
    pass

INPUT = lib.aoc.get_input(2023, 12)
part1(INPUT)
part2(INPUT)
