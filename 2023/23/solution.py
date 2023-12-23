import lib.aoc
import lib.graph
import lib.grid

def part1(s):
    grid = lib.grid.FixedGrid.parse(s)

    end_y = grid.height-1
    for x in grid.x_range:
        if grid[x,0] == '.':
            start = x,0
        if grid[x,end_y] == '.':
            end = x,end_y

    answer = 0
    best = None

    paths = [((start,),0)]

    while paths:
        new_paths = set()

        for p, d in paths:
            coord = p[-1]
            c = grid[coord]
            if c in '<>v^':
                x,y = coord
                if c == '<':
                    n = (x-1,y)
                elif c == '>':
                    n = (x+1,y)
                elif c == '^':
                    n = (x,y-1)
                elif c == 'v':
                    n = (x,y+1)
                if n not in p:
                    new_paths.add((p + (n,), d+1))
                continue
            else:
                assert(c == '.')
            for n in grid.neighbors(*coord):
                if n in p:
                    continue
                if n == end:
                    dist = d+1
                    if dist > answer:
                        answer = dist
                        best = p + (n,)
                    continue
                if grid[n] == '#':
                    continue
                new_paths.add((p + (n,), d+1))

        paths = new_paths

    lib.aoc.give_answer(2023, 23, 1, answer)

def part2(s):
    grid = lib.grid.FixedGrid.parse(s)

    end_y = grid.height-1
    for x in grid.x_range:
        if grid[x,0] == '.':
            start = x,0
        if grid[x,end_y] == '.':
            end = x,end_y

    def neighbor_fn(coord):
        x,y = coord

        handled = {coord}
        todo = [(n, 1) for n in grid.neighbors(*coord)
                if grid[n] != '#']

        while todo:
            c, d = todo.pop()
            handled.add(c)

            if c == end:
                yield c, d
                continue

            neighbors = list(grid.neighbors(*c))

            neighbors = [n for n in neighbors
                         if n not in handled
                         if grid[n] != '#']

            if len(neighbors) == 0:
                continue

            if len(neighbors) > 1:
                # Intersection
                yield c, d
                continue

            n = neighbors[0]
            todo.append((n, d+1))

    graph = lib.graph.make_lazy_graph(neighbor_fn)

    todo = [start]

    seen = set()
    while todo:
        coord = todo.pop()
        if coord in seen:
            continue
        seen.add(coord)

        for n, _ in graph[coord]:
            todo.append(n)

    answer = 0

    paths = [((start,),0)]

    while paths:
        new_paths = set()

        for p, d in paths:
            for n, n_d in graph[p[-1]]:
                if n in p:
                    continue
                if n == end:
                    answer = max(answer, d+n_d)
                    continue
                new_paths.add((p + (n,), d+n_d))

        paths = new_paths

    lib.aoc.give_answer(2023, 23, 2, answer)

INPUT = lib.aoc.get_input(2023, 23)
part1(INPUT)
part2(INPUT)
