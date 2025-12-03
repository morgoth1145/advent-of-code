import lib.aoc
import lib.grid

def find_max_as_arr(r, rem_items):
    if rem_items == 0:
        return []

    assert(rem_items <= len(r))

    best_i = None
    best = -1

    for i, v in enumerate(r):
        if len(r) - i - 1 < rem_items - 1:
            break

        if v > best:
            best = v
            best_i = i

    return [best] + find_max_as_arr(r[best_i+1:], rem_items-1)

def find_max(r, num_items):
    a = find_max_as_arr(r, num_items)
    assert(len(a) == num_items)
    return int(''.join(map(str, a)))

def part1(s):
    grid = lib.grid.FixedGrid.parse(s, value_fn=int)

    answer = 0

    for y in grid.y_range:
        r = grid.row(y)
        answer += find_max(r, 2)

    lib.aoc.give_answer(2025, 3, 1, answer)

def part2(s):
    grid = lib.grid.FixedGrid.parse(s, value_fn=int)

    answer = 0

    for i, y in enumerate(grid.y_range):
        r = grid.row(y)
        answer += find_max(r, 12)

    lib.aoc.give_answer(2025, 3, 2, answer)

INPUT = lib.aoc.get_input(2025, 3)
part1(INPUT)
part2(INPUT)
