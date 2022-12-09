import lib.aoc

def solve(s, rope_length):
    rope = [(0, 0)] * rope_length

    seen = set()
    seen.add(rope[-1])

    def do_move(dx, dy, c):
        nonlocal rope
        x, y = rope[0]
        for _ in range(c):
            x += dx
            y += dy
            new_rope = [(x, y)]
            for i, (nx, ny) in enumerate(rope[1:]):
                i += 1
                ax, ay = new_rope[i-1]
                bx, by = rope[i]
                if max(abs(ax-bx), abs(ay-by)) == 2:
                    if ax == bx:
                        by = (ay + by) // 2
                    elif ay == by:
                        bx = (ax + bx) // 2
                    else:
                        # Diagonal
                        ldx = ax - bx
                        ldy = ay - by
                        ldx //= abs(ldx)
                        ldy //= abs(ldy)
                        bx += ldx
                        by += ldy
                new_rope.append((bx, by))
            rope = new_rope
            seen.add(rope[-1])

    for line in s.splitlines():
        d, c = line.split()
        c = int(c)

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
