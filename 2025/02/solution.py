import lib.aoc

def part1(s):
    ranges = s.split(',')

    answer = 0

    for r in ranges:
        a, b = r.split('-')
        a = int(a)
        b = int(b)
        r = range(a, b+1)

        for i in r:
            istr = str(i)

            if len(istr) % 2 != 0:
                continue
            n = len(istr)
            fir = istr[:n//2]
            if fir*2 == istr:
                answer += i

    lib.aoc.give_answer(2025, 2, 1, answer)

def part2(s):
    pass

INPUT = lib.aoc.get_input(2025, 2)
part1(INPUT)
part2(INPUT)
