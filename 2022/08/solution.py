import lib.aoc
import lib.grid

def get_tree_stats(s):
    grid = lib.grid.FixedGrid.parse(s, value_fn=int)

    for (x, y), self_height in grid.items():
        obscured = True
        distances = []

        for dx, dy in [(-1, 0),
                       (1, 0),
                       (0, -1),
                       (0, 1)]:
            nx, ny = x, y
            num_trees_visible = 0
            while True:
                nx, ny = nx+dx, ny+dy
                if (nx, ny) not in grid:
                    obscured = False
                    break
                num_trees_visible += 1
                if grid[nx, ny] >= self_height:
                    break # Obscured
            distances.append(num_trees_visible)

        yield distances, obscured

def part1(s):
    answer = sum(1
                 for _, obscured in get_tree_stats(s)
                 if not obscured)

    lib.aoc.give_answer(2022, 8, 1, answer)

def part2(s):
    def score(distances):
        t = 1
        for dist in distances:
            t *= dist
        return t

    answer = max(score(distances)
                 for distances, _ in get_tree_stats(s))

    lib.aoc.give_answer(2022, 8, 2, answer)

INPUT = lib.aoc.get_input(2022, 8)
part1(INPUT)
part2(INPUT)
