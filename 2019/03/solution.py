import lib.aoc

def parse_wire(instructions):
    wire = {}

    x, y = 0, 0

    steps = 0
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
            steps += 1

            wire[x,y] = wire.get((x, y), steps)

    return wire

def part1(s):
    w1, w2 = s.splitlines()

    w1 = parse_wire(w1)
    w2 = parse_wire(w2)

    answer = min(abs(x) + abs(y)
                 for (x, y) in w1
                 if (x, y) in w2)

    lib.aoc.give_answer(2019, 3, 1, answer)

def part2(s):
    w1, w2 = s.splitlines()

    w1 = parse_wire(w1)
    w2 = parse_wire(w2)

    answer = min(w1[c] + w2[c]
                 for c in w1
                 if c in w2)

    lib.aoc.give_answer(2019, 3, 2, answer)

INPUT = lib.aoc.get_input(2019, 3)
part1(INPUT)
part2(INPUT)
