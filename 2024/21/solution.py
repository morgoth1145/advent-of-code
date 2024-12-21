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
KEYPAD2_GRAPH = make_keypad_graph()

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
def possible_keypad_move_sequences(start, end):
    out = []
    for p, dist in lib.graph.find_shortest_paths(KEYPAD_GRAPH,
                                                 POSITIONS[start],
                                                 POSITIONS[end]):
        out_p = ''.join(path_to_directions(p))
        out.append(out_p)
    return out

def calc_repetition(seq):
    out = 0

    for c, c2 in zip(seq, seq[1:]):
        if c == c2:
            out += 1

    return out

def shortest_sequences(seq):
    start = 'A'

    candidates = ['']

    for c in seq:
        new_cands = set()

        for option in possible_keypad_move_sequences(start, c):
            for cand in candidates:
                new_cands.add(cand + option)

        candidates = sorted(new_cands)
        start = c

    min_len = min(map(len, candidates))
    candidates = [c for c in candidates if len(c) == min_len]

    best_rep = max(map(calc_repetition, candidates))
    candidates = [c for c in candidates if calc_repetition(c) == best_rep]

    return candidates

@functools.cache
def possible_keypad2_move_sequences(start, end):
    out = []
    for p, dist in lib.graph.find_shortest_paths(KEYPAD2_GRAPH,
                                                 POSITIONS2[start],
                                                 POSITIONS2[end]):
        out_p = ''.join(path_to_directions(p))
        out.append(out_p)
    return out

def shortest_sequences2(seq):
    start = 'A'

    candidates = ['']

    for c in seq:
        new_cands = set()

        for option in possible_keypad2_move_sequences(start, c):
            for cand in candidates:
                new_cands.add(cand + option)

        candidates = sorted(new_cands)
        start = c

    min_len = min(map(len, candidates))
    candidates = [c for c in candidates if len(c) == min_len]

    best_rep = max(map(calc_repetition, candidates))
    candidates = [c for c in candidates if calc_repetition(c) == best_rep]

    return candidates

def part1(s):
    data = s.splitlines()

    answer = 0

    for line in data:
        outer_candidates = set()
        for inner_seq in shortest_sequences(line):
            for outer_seq in shortest_sequences2(inner_seq):
                outer_candidates.add(outer_seq)

        best_outer_len = min(map(len, outer_candidates))

        outer2_candidates = set()
        for c in sorted(outer_candidates):
            if len(c) == best_outer_len:
                for outer2_seq in shortest_sequences2(c):
                    outer2_candidates.add(outer2_seq)

        best_outer2_len = min(map(len, outer2_candidates))

        answer += best_outer2_len * int(line[:-1])

    answer = answer

    lib.aoc.give_answer(2024, 21, 1, answer)

def part2(s):
    pass

INPUT = lib.aoc.get_input(2024, 21)
part1(INPUT)
part2(INPUT)
