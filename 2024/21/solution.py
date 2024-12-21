import functools

import lib.aoc
import lib.graph
import lib.grid

def calc_keypad_moves(keypad_grid_str):
    grid = lib.grid.FixedGrid.parse(keypad_grid_str)

    def neighbor_fn(key):
        pos = grid.find(key)

        for n in grid.neighbors(*pos):
            if grid[n] == '#':
                continue
            yield grid[n], 1

    graph = lib.graph.make_lazy_graph(neighbor_fn)

    keypad_moves = {}

    for _, first in grid.items():
        if first == '#':
            continue
        for _, second in grid.items():
            if second == '#':
                continue
            paths = []
            for p, _ in lib.graph.find_shortest_paths(graph, first, second):
                path = ''
                for key1, key2 in zip(p, p[1:]):
                    x1, y1 = grid.find(key1)
                    x2, y2 = grid.find(key2)
                    dx, dy = x2-x1, y2-y1
                    move = {(-1, 0): '<',
                            (1, 0): '>',
                            (0, 1): 'v',
                            (0, -1): '^'}[dx,dy]
                    path += move
                # Make sure to press the button at the end!
                paths.append(path + 'A')
            keypad_moves[first,second] = paths

    return keypad_moves

def solve(s, num_robots):
    NUM_KEYPAD_MOVES = calc_keypad_moves('''789
456
123
#0A''')
    DIR_KEYPAD_MOVES = calc_keypad_moves('''#^A
<v>''')

    @functools.cache
    def dir_keypresses_for_dir_seq(seq, num_robots_left):
        if num_robots_left == 0:
            return len(seq)

        return sum(min(dir_keypresses_for_dir_seq(cand, num_robots_left-1)
                       for cand
                       in DIR_KEYPAD_MOVES[src, dest])
                   for src, dest
                   in zip('A' + seq, seq))

    def dir_keypresses_for_num_seq(seq):
        return sum(min(dir_keypresses_for_dir_seq(cand, num_robots)
                       for cand
                       in NUM_KEYPAD_MOVES[src, dest])
                   for src, dest
                   in zip('A' + seq, seq))

    return sum(int(line[:-1]) * dir_keypresses_for_num_seq(line)
               for line
               in s.splitlines())

def part1(s):
    answer = solve(s, 2)

    lib.aoc.give_answer(2024, 21, 1, answer)

def part2(s):
    answer = solve(s, 25)

    lib.aoc.give_answer(2024, 21, 2, answer)

INPUT = lib.aoc.get_input(2024, 21)
part1(INPUT)
part2(INPUT)
