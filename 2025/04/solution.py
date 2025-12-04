import lib.aoc
import lib.grid

def solve(s, max_layers=None):
    grid = lib.grid.FixedGrid.parse(s)

    # Convert grid to a dict of tp to neighbor counts
    # This helps limit work in subsequent iterations making everything faster
    tp_neighbor_counts = {
        pos: sum(grid[n] == '@'
                 for n
                 in grid.neighbors(*pos, diagonals=True))
        for pos, c in grid.items()
        if c == '@'
    }

    answer = 0

    to_check = list(tp_neighbor_counts.keys())

    while to_check:
        to_remove = [pos for pos in to_check
                     if tp_neighbor_counts.get(pos, 4) < 4]

        answer += len(to_remove)

        # Record which cells have been affected to minimize redundant checks
        new_to_check = set()

        for pos in to_remove:
            del tp_neighbor_counts[pos]

            for n in grid.neighbors(*pos, diagonals=True):
                new_c = tp_neighbor_counts.get(n)
                if new_c is None:
                    continue
                tp_neighbor_counts[n] = new_c - 1
                new_to_check.add(n)

        if max_layers is not None:
            max_layers -= 1
            if max_layers == 0:
                break

        to_check = new_to_check

    return answer

def part1(s):
    answer = solve(s, max_layers=1)

    lib.aoc.give_answer(2025, 4, 1, answer)

def part2(s):
    answer = solve(s)

    lib.aoc.give_answer(2025, 4, 2, answer)

INPUT = lib.aoc.get_input(2025, 4)
part1(INPUT)
part2(INPUT)
