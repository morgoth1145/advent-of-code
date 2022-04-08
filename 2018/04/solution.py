import collections

import lib.aoc

def parse_sleep_record(s):
    guard_sleep_record = collections.defaultdict(collections.Counter)

    duty = None
    fell_asleep = None

    for line in sorted(s.splitlines()):
        date, time, act = line.split(maxsplit=2)
        date = date[1:]

        hour, minute = list(map(int, time[:-1].split(':')))

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

    return guard_sleep_record

def part1(s):
    guard_sleep_record = parse_sleep_record(s)

    guard, sleep_record = max(guard_sleep_record.items(),
                              key=lambda pair: sum(pair[1].values()))
    (minute, _), = sleep_record.most_common(1)

    answer = guard * minute

    lib.aoc.give_answer(2018, 4, 1, answer)

def part2(s):
    guard_sleep_record = parse_sleep_record(s)

    best = (0, 0, 0)

    for guard, sleep_record in guard_sleep_record.items():
        (minute, times_slept), = sleep_record.most_common(1)
        best = max(best, (times_slept, guard, minute))

    _, guard, minute = best

    answer = guard * minute

    lib.aoc.give_answer(2018, 4, 2, answer)

INPUT = lib.aoc.get_input(2018, 4)
part1(INPUT)
part2(INPUT)
