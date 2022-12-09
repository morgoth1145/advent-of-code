import lib.aoc

def parse_input(s):
    for line in s.splitlines():
        a, b = line.split()
        yield a, int(b)

def part1(s):
    head = (0, 0)
    tail = (0, 0)

    seen = set()
    seen.add(tail)

    def do_move(dx, dy, c):
        nonlocal head, tail
        x, y = head
        tx, ty = tail
        for _ in range(c):
            x += dx
            y += dy
            if max(abs(x-tx), abs(y-ty)) == 2:
                tx = x - dx
                ty = y - dy
                seen.add((tx, ty))
        head = (x, y)
        tail = (tx, ty)

    for d, c in parse_input(s):
        if d == 'U':
            do_move(0, -1, c)
        elif d == 'D':
            do_move(0, 1, c)
        elif d == 'L':
            do_move(-1, 0, c)
        elif d == 'R':
            do_move(1, 0, c)
        else:
            assert(False)

    answer = len(seen)

    lib.aoc.give_answer(2022, 9, 1, answer)

def part2(s):
    pass

INPUT = lib.aoc.get_input(2022, 9)
part1(INPUT)
part2(INPUT)
