import lib.aoc

def parse_input(s):
    ranges, nums = s.split('\n\n')

    ranges = [tuple(map(int, l.split('-')))
              for l in ranges.splitlines()]
    ranges = [range(int(a), int(b)+1)
              for a, b in ranges]
    nums = list(map(int, nums.splitlines()))

    return ranges, nums

def part1(s):
    ranges, nums = parse_input(s)

    answer = sum(any(n in r for r in ranges)
                 for n in nums)

    lib.aoc.give_answer(2025, 5, 1, answer)

def part2(s):
    ranges, _ = parse_input(s)

    ranges = sorted(ranges, key=lambda r: (r.start, r.stop))

    answer = 0

    while len(ranges) > 1:
        r0 = ranges.pop(0)
        r1 = ranges[0]

        if r0.stop <= r1.start:
            answer += len(r0)
        else:
            ranges[0] = range(r0.start, max(r0.stop, r1.stop))

    answer += len(ranges.pop())

    lib.aoc.give_answer(2025, 5, 2, answer)

INPUT = lib.aoc.get_input(2025, 5)
part1(INPUT)
part2(INPUT)
