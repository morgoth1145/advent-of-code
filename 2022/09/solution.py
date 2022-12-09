import lib.aoc

def head_positions(s):
    x, y = 0, 0
    yield x, y

    for line in s.splitlines():
        d, c = line.split()

        if d == 'U': dx, dy = 0, -1
        elif d == 'D': dx, dy = 0, 1
        elif d == 'L': dx, dy = -1, 0
        elif d == 'R': dx, dy = 1, 0

        for _ in range(int(c)):
            x, y = x+dx, y+dy
            yield x, y

def next_segment_positions(positions):
    x, y = 0, 0
    yield x, y

    for prev_x, prev_y in positions:
        dx, dy = prev_x-x, prev_y-y

        if max(abs(dx), abs(dy)) == 2:
            # This segment needs to move to catch up!
            if dx != 0:
                x += dx // abs(dx)
            if dy != 0:
                y += dy // abs(dy)
            yield x, y

def part1(s):
    answer = len(set(next_segment_positions(head_positions(s))))

    lib.aoc.give_answer(2022, 9, 1, answer)

def part2(s):
    rope = head_positions(s)
    for _ in range(9):
        rope = next_segment_positions(rope)
    answer = len(set(rope))

    lib.aoc.give_answer(2022, 9, 2, answer)

INPUT = lib.aoc.get_input(2022, 9)
part1(INPUT)
part2(INPUT)
