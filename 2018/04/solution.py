import collections

import lib.aoc

def parse_input(s):
    for line in sorted(s.splitlines()):
        date, time, act = line.split(maxsplit=2)
        date = date[1:]

        hour, minute = list(map(int, time[:-1].split(':')))

        yield date, hour, minute, act

def part1(s):
    guard_sleep_record = collections.defaultdict(collections.Counter)

    duty = None
    fell_asleep = None

    for date, hour, minute, act in parse_input(s):
        if act.startswith('Guard'):
            assert(fell_asleep is None)
            _, n, _, _ = act.split()
            duty = int(n[1:])
            continue
        assert(hour == 0)
        if act == 'falls asleep':
            assert(fell_asleep is None)
            fell_asleep = (date, minute)
            continue
        if act == 'wakes up':
            assert(fell_asleep is not None)
            assert(date == fell_asleep[0])
            for m in range(fell_asleep[1], minute):
                guard_sleep_record[duty][m] += 1
            fell_asleep = None
            continue
        assert(False)

    guard, sleep_record = max(guard_sleep_record.items(),
                              key=lambda pair: sum(pair[1].values()))
    (minute, _), = sleep_record.most_common(1)

    answer = guard * minute

    print(f'The answer to part one is {answer}')

def part2(s):
    pass

INPUT = lib.aoc.get_input(2018, 4)
part1(INPUT)
part2(INPUT)
