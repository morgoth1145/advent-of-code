import lib.aoc

def solve(s, rope_length):
    rope = [(0, 0)] * rope_length

    seen = set()
    seen.add(rope[-1])

    def do_move(dx, dy, c):
        for _ in range(c):
            x, y = rope[0]
            rope[0] = x, y = x+dx, y+dy
            for i, (nx, ny) in enumerate(rope[1:]):
                ldx, ldy = x - nx, y - ny

                if max(abs(ldx), abs(ldy)) == 2:
                    # Move in the same row/column if possible,
                    # or move diagonally if necessary
                    if ldx != 0:
                        nx += ldx // abs(ldx)
                    if ldy != 0:
                        ny += ldy // abs(ldy)

                x, y = rope[i+1] = nx, ny

            seen.add(rope[-1])

    for line in s.splitlines():
        d, c = line.split()
        c = int(c)

        if d == 'U': do_move(0, -1, c)
        elif d == 'D': do_move(0, 1, c)
        elif d == 'L': do_move(-1, 0, c)
        elif d == 'R': do_move(1, 0, c)

    return len(seen)

def part1(s):
    answer = solve(s, 2)

    lib.aoc.give_answer(2022, 9, 1, answer)

def part2(s):
    answer = solve(s, 10)

    lib.aoc.give_answer(2022, 9, 2, answer)

INPUT = lib.aoc.get_input(2022, 9)
part1(INPUT)
part2(INPUT)
