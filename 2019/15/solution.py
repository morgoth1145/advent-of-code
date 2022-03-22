import lib.aoc
import lib.graph

intcode = __import__('2019.intcode').intcode

def part1(s):
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

    def neighbor_fn(coord):
        x, y = coord
        for n in [(x, y-1),
                  (x, y+1),
                  (x-1, y),
                  (x+1, y)]:
            if grid[n] != '#':
                yield n, 1

    graph = lib.graph.make_lazy_graph(neighbor_fn)

    answer = lib.graph.dijkstra_length(graph, (0, 0), oxy_coord)

    print(f'The answer to part one is {answer}')

def part2(s):
    pass

INPUT = lib.aoc.get_input(2019, 15)
part1(INPUT)
part2(INPUT)
