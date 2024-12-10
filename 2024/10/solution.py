import lib.aoc
import lib.grid

def solve(s, bfs_collection_type):
    grid = lib.grid.FixedGrid.parse(s, value_fn=int)

    def score_trailhead(coord):
        states = bfs_collection_type([coord])

        # Walk the states from 0 up to 9
        for target_val in range(1, 10):
            states = bfs_collection_type(n
                                         for coord in states
                                         for n in grid.neighbors(*coord)
                                         if grid[n] == target_val)

        return len(states)

    return sum(map(score_trailhead, grid.coords_by_value()[0]))

def part1(s):
    # Count only unique destinations
    answer = solve(s, set)

    lib.aoc.give_answer(2024, 10, 1, answer)

def part2(s):
    # Use list to count all paths
    answer = solve(s, list)

    lib.aoc.give_answer(2024, 10, 2, answer)

INPUT = lib.aoc.get_input(2024, 10)
part1(INPUT)
part2(INPUT)
