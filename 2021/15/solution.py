import lib.aoc
import lib.graph
import lib.grid

def solve(grid):
    graph = {}

    for c, val in grid.items():
        x, y = c
        graph[c] = [(n, grid[n])
                    for n in grid.neighbors(x, y)]

    X = grid.width-1
    Y = grid.height-1

    return lib.graph.dijkstra_length(graph, (0, 0), (X, Y))

def part1(s):
    grid = lib.grid.FixedGrid.parse(s, value_fn=int)
    answer = solve(grid)

    lib.aoc.give_answer(2021, 15, 1, answer)

def part2(s):
    grid = lib.grid.FixedGrid.parse(s, value_fn=int)

    # TODO: Is there a way to do this less horribly? This feels so hacky!
    d = grid.to_dict()
    for xadj in range(5):
        for yadj in range(5):
            adj = xadj + yadj
            if adj == 0:
                continue

            xshift = grid.width * xadj
            yshift = grid.height * yadj

            for c, val in grid.items():
                x, y = c
                newc = x + xshift, y + yshift
                d[newc] = (val + adj - 1) % 9 + 1
    grid = lib.grid.FixedGrid.from_dict(d)

    answer = solve(grid)

    lib.aoc.give_answer(2021, 15, 2, answer)

INPUT = lib.aoc.get_input(2021, 15)
part1(INPUT)
part2(INPUT)
