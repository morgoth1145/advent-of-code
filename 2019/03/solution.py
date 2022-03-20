import lib.aoc

def parse_wire(instructions):
    wire = set()

    x, y = 0, 0

    for inst in instructions.split(','):
        direct = inst[0]
        count = int(inst[1:])

        if direct == 'U':
            dx, dy = 0, 1
        elif direct == 'D':
            dx, dy = 0, -1
        elif direct == 'L':
            dx, dy = -1, 0
        elif direct == 'R':
            dx, dy = 1, 0
        else:
            assert(False)

        for _ in range(count):
            x, y = x+dx, y+dy
            wire.add((x, y))

    return wire

def part1(s):
    w1, w2 = s.splitlines()

    w1 = parse_wire(w1)
    w2 = parse_wire(w2)

    answer = min(abs(x) + abs(y)
                 for x, y in w1
                 if (x, y) in w2)

    print(f'The answer to part one is {answer}')

def part2(s):
    pass

INPUT = lib.aoc.get_input(2019, 3)
part1(INPUT)
part2(INPUT)
