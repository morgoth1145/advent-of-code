import functools

import lib.aoc

def decompress(s):
    out = ''

    while s:
        idx = s.find('(')
        if idx == -1:
            assert(')' not in s)
            out += s
            s = ''
            continue
        end_idx = s.find(')')
        assert(end_idx > idx)

        out += s[:idx]
        marker = s[idx+1:end_idx]
        s = s[end_idx+1:]

        l, c = marker.split('x')
        l = int(l)
        c = int(c)

        take = s[:l]
        s = s[l:]
        for _ in range(c):
            out += take

    return out

def part1(s):
    answer = len(decompress(s))

    lib.aoc.give_answer(2016, 9, 1, answer)

@functools.cache
def decompress_2_length(s):
    length = 0

    while s:
        idx = s.find('(')
        if idx == -1:
            assert(')' not in s)
            length += len(s)
            s = ''
            continue

        end_idx = s.find(')')
        assert(end_idx > idx)

        length += idx
        marker = s[idx+1:end_idx]
        s = s[end_idx+1:]

        l, c = marker.split('x')
        l = int(l)
        c = int(c)

        take = s[:l]
        s = s[l:]

        length += c * decompress_2_length(take)

    return length

def part2(s):
    answer = decompress_2_length(s)

    lib.aoc.give_answer(2016, 9, 2, answer)

INPUT = lib.aoc.get_input(2016, 9)
part1(INPUT)
part2(INPUT)
