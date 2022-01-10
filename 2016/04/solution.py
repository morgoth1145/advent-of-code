import collections

import lib.aoc

def parse_input(s):
    for line in s.splitlines():
        assert(line[-7] == '[')
        assert(line[-1] == ']')
        checksum = line[-6:-1]
        room = line[:-7]
        idx = room.rfind('-')
        sector = room[idx+1:]
        room = room[:idx]
        yield room, int(sector), checksum

def part1(s):
    answer = 0

    for room, sector, checksum in parse_input(s):
        counts = collections.Counter(room.replace('-', ''))
        counts = sorted(counts.most_common(),
                        key=lambda p: (-p[1],p[0]))[:5]
        real_checksum = ''.join(c[0] for c in counts)
        if checksum == real_checksum:
            answer += sector

    print(f'The answer to part one is {answer}')

def part2(s):
    pass

INPUT = lib.aoc.get_input(2016, 4)
part1(INPUT)
part2(INPUT)
