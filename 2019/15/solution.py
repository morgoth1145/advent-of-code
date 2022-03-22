import lib.aoc
import lib.graph

intcode = __import__('2019.intcode').intcode

def parse_grid(s):
    in_chan, out_chan = intcode.Program(s).run(stop_on_no_input=True)

    grid = {}

    def explore(x, y):
        for move, inverse, nx, ny in [(1, 2, x, y-1),
                                      (2, 1, x, y+1),
                                      (3, 4, x-1, y),
                                      (4, 3, x+1, y)]:
            if (nx, ny) in grid:
                # We already know about that cell!
                continue
            in_chan.send(move)
            status = out_chan.recv()

            if status == 0:
                grid[nx,ny] = '#'
                continue

            if status == 1:
                grid[nx,ny] = '.'
            else:
                assert(status == 2)
                grid[nx,ny] = 'O'

            # New cell, explore it
            explore(nx,ny)
            # Now back track
            in_chan.send(inverse)
            out_chan.recv() # Ignore the status

    explore(0, 0)

    # Tell the program to close
    in_chan.close()

    oxy_coord = None
    for coord, contents in grid.items():
        if contents == 'O':
            oxy_coord = coord
            break

    return grid, oxy_coord

def neighbor_coords(x, y):
    return [(x, y-1),
            (x, y+1),
            (x-1, y),
            (x+1, y)]

def part1(s):
    grid, oxy_coord = parse_grid(s)

    def neighbor_fn(coord):
        for n in neighbor_coords(*coord):
            if grid[n] != '#':
                yield n, 1

    graph = lib.graph.make_lazy_graph(neighbor_fn)

    answer = lib.graph.dijkstra_length(graph, (0, 0), oxy_coord)

    print(f'The answer to part one is {answer}')

def part2(s):
    grid, oxy_coord = parse_grid(s)

    def open_neighbors(cells):
        for x, y in cells:
            for n in neighbor_coords(x, y):
                if grid[n] == '.':
                    yield n

    answer = 0

    next_to_fill = set(open_neighbors([oxy_coord]))

    while next_to_fill:
        answer += 1
        for c in next_to_fill:
            grid[c] = 'O'
        next_to_fill = set(open_neighbors(next_to_fill))

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2019, 15)
part1(INPUT)
part2(INPUT)
