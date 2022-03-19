import sys

import lib.aoc

# UTTER HACK
sys.setrecursionlimit(3000)

def parse_clay(s):
    clay = set()
    for line in s.splitlines():
        a, b = line.split(', ')
        pos = int(a[2:])
        rs, re = list(map(int, b[2:].split('..')))
        r = range(rs, re+1)

        if a[0] == 'x':
            for y in r:
                clay.add((pos, y))
        else:
            for x in r:
                clay.add((x, pos))
    return clay

def part1(s):
    clay = parse_clay(s)

    min_y = min(y for x,y in clay)
    max_y = max(y for x,y in clay)

    seen = set()
    supports = set(clay)

    def flood(x, y):
        if y > max_y:
            return

        if (x, y) in seen:
            return

        if y >= min_y:
            seen.add((x, y))

        if (x, y+1) not in clay:
            flood(x, y+1)

        if (x, y+1) in supports:
            supported = True
            row = [(x, y)]

            left_x = x-1
            while (left_x, y) not in clay:
                row.append((left_x, y))
                if (left_x, y+1) not in supports:
                    flood(left_x, y+1)
                if (left_x, y+1) not in supports:
                    supported = False
                    break
                left_x -= 1

            right_x = x+1
            while (right_x, y) not in clay:
                row.append((right_x, y))
                if (right_x, y+1) not in supports:
                    flood(right_x, y+1)
                if (right_x, y+1) not in supports:
                    supported = False
                    break
                right_x += 1

            seen.update(row)

            if supported:
                supports.update(row)

    flood(500, 0)

    answer = len(seen)

    print(f'The answer to part one is {answer}')

def part2(s):
    pass

INPUT = lib.aoc.get_input(2018, 17)
part1(INPUT)
part2(INPUT)
