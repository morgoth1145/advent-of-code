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

    answer = 0

    while ranges:
        r = ranges.pop()

        good = True
        for r2 in ranges:
            if r2.start < r.stop and r2.stop > r.start:
                ranges.append(range(r.start, r2.start))
                ranges.append(range(r2.stop, r.stop))
                good = False
                break

        if good:
            answer += len(r)

    lib.aoc.give_answer(2025, 5, 2, answer)

INPUT = lib.aoc.get_input(2025, 5)
part1(INPUT)
part2(INPUT)
