import lib.aoc
import lib.graph
import lib.grid

def solve(s):
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
            coord, d = todo.pop()
            assert(coord not in handled)
            handled.add(coord)

            if coord == end:
                yield coord, d
                continue

            c = grid[coord]
            if c in '<>v^':
                x,y = coord
                if c == '<':
                    n = (x-1,y)
                elif c == '>':
                    n = (x+1,y)
                elif c == 'v':
                    n = (x,y+1)
                elif c == '^':
                    n = (x,y-1)
                if n not in handled:
                    todo.append((n, d+1))
                continue
            else:
                assert(c == '.')

            neighbors = [n for n in grid.neighbors(*coord)
                         if grid[n] != '#']

            if len(neighbors) > 2:
                # Intersection
                yield coord, d
                continue

            neighbors = [n for n in neighbors
                         if n not in handled]

            if len(neighbors) == 0:
                continue

            n = neighbors[0]
            todo.append((n, d+1))

    graph = lib.graph.make_lazy_graph(neighbor_fn)

    def longest_path(path, dist):
        best = -1
        for n, n_dist in graph[path[-1]]:
            if n in path:
                continue
            if n == end:
                best = max(best, dist + n_dist)
                continue

            best = max(best, longest_path(path + (n,), dist + n_dist))

        return best

    return longest_path((start,), 0)

def part1(s):
    answer = solve(s)

    lib.aoc.give_answer(2023, 23, 1, answer)

def part2(s):
    for c in '<>^v':
        s = s.replace(c, '.')

    answer = solve(s)

    lib.aoc.give_answer(2023, 23, 2, answer)

INPUT = lib.aoc.get_input(2023, 23)
part1(INPUT)
part2(INPUT)
