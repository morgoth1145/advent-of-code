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

def count_matches2(pattern, splits):
    @functools.cache
    def gen(rem_pattern, rem_len, rem_splits):
        if len(rem_splits) == 0:
            if all(c in '.?' for c in rem_pattern):
                return 1
            return 0

        a = rem_splits[0]
        rest = rem_splits[1:]
        after = sum(rest) + len(rest)

        count = 0

        for before in range(rem_len-after-a+1):
            cand = '.' * before + '#' * a + '.'
            if all(c0 == c1 or c0=='?'
                   for c0,c1 in zip(rem_pattern, cand)):
                rest_pattern = rem_pattern[len(cand):]
                count += gen(rest_pattern, rem_len-a-before-1, rest)

        return count

    return gen(pattern, len(pattern), tuple(splits))

def part2(s):
    data = list(parse_input(s))

    answer = 0

    for a, b in data:
        answer += count_matches2('?'.join((a,a,a,a,a)), b*5)

    lib.aoc.give_answer(2023, 12, 2, answer)

INPUT = lib.aoc.get_input(2023, 12)
part1(INPUT)
part2(INPUT)
