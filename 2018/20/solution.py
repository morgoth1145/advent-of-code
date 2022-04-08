import collections

import lib.aoc
import lib.graph

def contruct_map(s):
    assert(s[0] == '^')
    assert(s[-1] == '$')

    MOVES = {
        'N': lambda x,y: (x, y-1),
        'S': lambda x,y: (x, y+1),
        'E': lambda x,y: (x+1, y),
        'W': lambda x,y: (x-1, y),
    }

    m = collections.defaultdict(set)

    stack = []
    base_positions = None
    positions = {(0, 0)}

    for c in s[1:-1]:
        if c in MOVES:
            new_positions = set()
            for x, y in positions:
                n = MOVES[c](x, y)
                m[x,y].add((n, 1))
                m[n].add(((x,y), 1))
                new_positions.add(n)
            positions = new_positions
        elif c == '(':
            stack.append((set(), base_positions))
            base_positions = positions
        elif c == '|':
            # Propagate positions back up the stack
            stack[-1][0].update(positions)
            # New set of options
            positions = base_positions
        elif c == ')':
            # Propagate positions back up the stack
            stack[-1][0].update(positions)
            # Pop back up
            positions, base_positions = stack.pop(-1)
        else:
            assert(False)

    assert(len(stack) == 0)

    return m

def part1(s):
    _, answer = lib.graph.longest_minimal_path_length(contruct_map(s), (0, 0))

    lib.aoc.give_answer(2018, 20, 1, answer)

def part2(s):
    answer = sum(1
                 for dest, dist
                 in lib.graph.all_reachable(contruct_map(s), (0, 0))
                 if dist >= 1000)

    lib.aoc.give_answer(2018, 20, 2, answer)

INPUT = lib.aoc.get_input(2018, 20)
part1(INPUT)
part2(INPUT)
