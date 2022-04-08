import lib.aoc
import lib.ocr

def apply_instructions(s):
    on_pixels = set()

    for inst in s.splitlines():
        parts = inst.split()
        if parts[0] == 'rect':
            w, h = parts[1].split('x')
            w = int(w)
            h = int(h)
            for x in range(w):
                for y in range(h):
                    on_pixels.add((x, y))
            continue

        n = int(parts[2][2:])
        by = int(parts[4])
        if parts[1] == 'row':
            new_on = set()
            for x, y in on_pixels:
                if y == n:
                    x = (x + by) % 50
                new_on.add((x, y))
            on_pixels = new_on
        else:
            assert(parts[1] == 'column')
            new_on = set()
            for x, y in on_pixels:
                if x == n:
                    y = (y + by) % 6
                new_on.add((x, y))
            on_pixels = new_on

    return on_pixels

def part1(s):
    answer = len(apply_instructions(s))

    lib.aoc.give_answer(2016, 8, 1, answer)

def part2(s):
    answer = lib.ocr.parse_coord_set(apply_instructions(s))

    lib.aoc.give_answer(2016, 8, 2, answer)

INPUT = lib.aoc.get_input(2016, 8)
part1(INPUT)
part2(INPUT)
