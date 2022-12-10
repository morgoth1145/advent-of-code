import lib.aoc
import lib.ocr

def register_per_cycle(s):
    val_per_cycle = []

    x = 1
    for line in s.splitlines():
        inst = line.split()
        if inst[0] == 'noop':
            # Single cycle instruction
            val_per_cycle += [x]
        elif inst[0] == 'addx':
            # Two cycle instruction
            val_per_cycle += [x, x]
            x += int(inst[1])
        else:
            assert(False)

    return val_per_cycle

def part1(s):
    x_per_cycle = register_per_cycle(s)

    answer = sum(cycle * x_per_cycle[cycle-1]
                 for cycle in (20, 60, 100, 140, 180, 220))

    lib.aoc.give_answer(2022, 10, 1, answer)

def part2(s):
    lit_pixels = {(cycle % 40, cycle // 40)
                  for cycle, pos in enumerate(register_per_cycle(s))
                  if cycle % 40 in (pos-1, pos, pos+1)}

    answer = lib.ocr.parse_coord_set(lit_pixels)

    lib.aoc.give_answer(2022, 10, 2, answer)

INPUT = lib.aoc.get_input(2022, 10)
part1(INPUT)
part2(INPUT)
