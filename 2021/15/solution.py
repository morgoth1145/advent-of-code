import lib.aoc
import lib.graph
import lib.grid

def part1(s):
    grid = lib.grid.FixedGrid.parse(s, value_fn=int)

    graph = {}

    for c, val in grid.items():
        x, y = c
        links = []
        for n in grid.neighbors(x, y):
            val = grid[n]
            links.append((n, val))
        graph[c] = links

    X = grid.width-1
    Y = grid.height-1

    answer = lib.graph.dijkstra_length(graph, (0, 0), (X, Y))

    print(f'The answer to part one is {answer}')

def part2(s):
    grid = lib.grid.FixedGrid.parse(s, value_fn=int)

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
                val += adj
                while val > 9:
                    val -= 9
                d[newc] = val

    grid = lib.grid.FixedGrid.from_dict(d)

    graph = {}

    for c, val in grid.items():
        x, y = c
        links = []
        for n in grid.neighbors(x, y):
            val = grid[n]
            links.append((n, val))
        graph[c] = links

    X = grid.width-1
    Y = grid.height-1

    answer = lib.graph.dijkstra_length(graph, (0, 0), (X, Y))

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2021, 15)
part1(INPUT)
part2(INPUT)
