import functools

import lib.aoc
import lib.graph

POSITIONS = {
    '7': (0,0),
    '8': (1,0),
    '9': (2,0),
    '4': (0,1),
    '5': (1,1),
    '6': (2,1),
    '1': (0,2),
    '2': (1,2),
    '3': (2,2),
    '0': (1,3),
    'A': (2,3),
    }
POS_TO_KEY = {pos:key
              for key, pos
              in POSITIONS.items()}

def make_keypad_graph():
    def neighbor_fn(pos):
        x, y = pos

        for nx, ny in [(x-1, y),
                       (x+1, y),
                       (x, y-1),
                       (x, y+1)]:
            if nx < 0 or nx > 3 or ny < 0 or ny > 3:
                continue
            if nx == 0 and ny == 3:
                continue
            yield (nx, ny), 1

    return lib.graph.make_lazy_graph(neighbor_fn)
KEYPAD_GRAPH = make_keypad_graph()

POSITIONS2 = {
    '^': (1,0),
    'A': (2,0),
    '<': (0,1),
    'v': (1,1),
    '>': (2,1),
    }
POS2_TO_KEY = {pos:key
              for key, pos
               in POSITIONS2.items()}

def make_keypad2_graph():
    def neighbor_fn(pos):
        x, y = pos

        for nx, ny in [(x-1, y),
                       (x+1, y),
                       (x, y-1),
                       (x, y+1)]:
            if nx < 0 or nx > 3 or ny < 0 or ny > 1:
                continue
            if nx == 0 and ny == 0:
                continue
            yield (nx, ny), 1

    return lib.graph.make_lazy_graph(neighbor_fn)
KEYPAD2_GRAPH = make_keypad2_graph()

def path_to_directions(path):
    x, y = path[0]
    for nx, ny in path[1:]:
        dx, dy = nx-x, ny-y
        x, y = nx, ny
        yield {(1, 0): '>',
               (-1, 0): '<',
               (0, -1): '^',
               (0, 1): 'v'}[dx,dy]
    yield 'A'

@functools.cache
def all_possible_keypad_move_sequences(start, end):
    out = []
    for p, dist in lib.graph.find_shortest_paths(KEYPAD_GRAPH,
                                                 POSITIONS[start],
                                                 POSITIONS[end]):
        out_p = ''.join(path_to_directions(p))
        out.append(out_p)

    return out

@functools.cache
def all_possible_keypad2_move_sequences(start, end):
    out = []
    for p, dist in lib.graph.find_shortest_paths(KEYPAD2_GRAPH,
                                                 POSITIONS2[start],
                                                 POSITIONS2[end]):
        out_p = ''.join(path_to_directions(p))
        out.append(out_p)

    return out

@functools.cache
def count_key2presses_to_achieve(first, second, levels_remaining):
    best = None

    for seq in all_possible_keypad2_move_sequences(first, second):
        if levels_remaining == 0:
            cost = len(seq)
        else:
            cost = count_key2presses_for_seq(seq, levels_remaining)

        if best is None or best > cost:
            best = cost

    return best

@functools.cache
def count_key2presses_for_seq(seq, num_levels):
    assert(num_levels > 0)
    presses = 0

    for a, b in zip('A' + seq, seq):
        presses += count_key2presses_to_achieve(a, b, num_levels-1)

    return presses

def find_best_seq(toplevel, num_keypad2_levels):
    all_presses = 0

    for a, b in zip('A' + toplevel, toplevel):
        best = None

        for seq in all_possible_keypad_move_sequences(a, b):
            presses = count_key2presses_for_seq(seq, num_keypad2_levels)
            if best is None or best > presses:
                best = presses

        all_presses += best

    return all_presses

def solve(s, num_levels):
    data = s.splitlines()

    answer = 0

    for line in data:
        presses = find_best_seq(line, num_levels)
        answer += presses * int(line[:-1])

    return answer

def part1(s):
    answer = solve(s, 2)

    lib.aoc.give_answer(2024, 21, 1, answer)

def part2(s):
    answer = solve(s, 25)

    lib.aoc.give_answer(2024, 21, 2, answer)

INPUT = lib.aoc.get_input(2024, 21)
part1(INPUT)
part2(INPUT)
