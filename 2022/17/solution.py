import collections

import lib.aoc

TOWER_WIDTH = 7

ROCKS = [
    [(2, 0), (3, 0), (4, 0), (5, 0)], # Horizontal Line
    [(3, 0), (2, 1), (3, 1), (4, 1), (3, 2)], # Plus
    [(2, 0), (3, 0), (4, 0), (4, 1), (4, 2)], # L
    [(2, 0), (2, 1), (2, 2), (2, 3)], # Vertical Bar
    [(2, 0), (2, 1), (3, 0), (3, 1)], # Square
]

def run_sim(s, tower, start_rock_idx, jet_idx, total_rocks):
    for rock_idx in range(start_rock_idx, total_rocks):
        rock = ROCKS[rock_idx % len(ROCKS)]
        y_off = max(y for x,y in tower) + 4
        rock = [(x, y+y_off) for x, y in rock]

        while True:
            jet = s[jet_idx % len(s)]
            if jet == '<':
                dx = -1
            else:
                dx = 1
            jet_idx += 1
            new_rock = [(x+dx, y) for x, y in rock]
            if any(x < 0 or x >= TOWER_WIDTH for x, y in new_rock):
                new_rock = rock
            elif any(c in tower for c in new_rock):
                new_rock = rock
            rock = new_rock
            new_rock = [(x, y-1) for x,y in rock]
            if any(c in tower for c in new_rock):
                # It settled
                tower.update(rock)
                break

            rock = new_rock

    return tower

def part1(s):
    tower = {(x, 0) for x in range(TOWER_WIDTH)}

    tower = run_sim(s, tower, 0, 0, 2022)

    answer = max(y for x,y in tower)

    lib.aoc.give_answer(2022, 17, 1, answer)

def part2_impl(s):
    tower = {(x, 0) for x in range(TOWER_WIDTH)}

    jet_idx = 0

    TIMES = 1000000000000

    tower_heights = collections.defaultdict(list)

    for rock_idx in range(TIMES):
        start_key = (rock_idx % len(ROCKS), jet_idx % len(s))

        rock = ROCKS[rock_idx % len(ROCKS)]
        y_off = max(y for x,y in tower) + 4
        rock = [(x, y+y_off) for x, y in rock]

        move_x, move_y = 0, 0

        while True:
            jet = s[jet_idx % len(s)]
            if jet == '<':
                dx = -1
            else:
                dx = 1
            jet_idx += 1
            new_rock = [(x+dx, y) for x, y in rock]
            if any(x < 0 or x >= TOWER_WIDTH for x, y in new_rock):
                new_rock = rock
            elif any(c in tower for c in new_rock):
                new_rock = rock
            else:
                move_x += dx
            rock = new_rock
            new_rock = [(x, y-1) for x,y in rock]
            if any(c in tower for c in new_rock):
                # It settled
                tower.update(rock)

                key = (start_key, move_x, move_y)
                current_height = max(y for x,y in tower)

                info_for_move = tower_heights[key]

                layout = tuple(max(y-current_height
                                   for x,y in tower
                                   if x == tx)
                               for tx in range(TOWER_WIDTH))

                stats = (current_height, rock_idx, layout)

                if len(info_for_move) > 1:
                    last_diff = info_for_move[-1][0] - info_for_move[-2][0]
                    curr_diff = current_height - info_for_move[-1][0]

                    last_move_diff = info_for_move[-1][1] - info_for_move[-2][1]
                    curr_move_diff = rock_idx - info_for_move[-1][1]

                    last_layout = info_for_move[-1][2]

                    if (curr_diff == last_diff and
                        last_move_diff == curr_move_diff):
                        assert(stats[2] == info_for_move[-1][2])
                        remaining_times = TIMES - rock_idx - 1

                        cycle_length = rock_idx - info_for_move[-1][1]
                        cycles = remaining_times // cycle_length
                        total_jumpahead = cycles * cycle_length

                        jumped_tower = run_sim(s, tower,
                                               rock_idx + 1 + total_jumpahead,
                                               jet_idx, TIMES)

                        return max(y for x,y in jumped_tower) + curr_diff * cycles

                info_for_move.append(stats)
                break

            move_y -= 1

            rock = new_rock

    assert(False)

def part2(s):
    answer = part2_impl(s)

    lib.aoc.give_answer(2022, 17, 2, answer)

INPUT = lib.aoc.get_input(2022, 17)
part1(INPUT)
part2(INPUT)
