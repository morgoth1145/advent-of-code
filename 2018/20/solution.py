import collections

import lib.aoc
import lib.graph

INVERSES = dict(zip('NSEW', 'SNWE'))
MOVES = {
    'N': lambda x,y: (x, y-1),
    'S': lambda x,y: (x, y+1),
    'E': lambda x,y: (x+1, y),
    'W': lambda x,y: (x-1, y),
}

class Node:
    def __init__(self):
        self.seq = []

    def add(self, step):
        self.seq.append(step)

    def has_data(self):
        return len(self.seq) > 0

def contruct_map(s):
    assert(s[0] == '^')
    assert(s[-1] == '$')
    s = s[1:-1]

    stack = [[Node()]]

    for c in s:
        if c in 'NSEW':
            stack[-1][-1].add(c)
        elif c == '(':
            stack.append([Node()])
        elif c == '|':
            stack[-1].append(Node())
        elif c == ')':
            children = stack.pop(-1)
            children = [c for c in children
                        if c.has_data()]
            stack[-1][-1].add(children)
            pass
        else:
            assert(False)

    assert(len(stack) == 1)
    assert(len(stack[0]) == 1)
    tree = stack[0][0]

    m = collections.defaultdict(set)

    def walk_tree(node, positions):
        for step in node.seq:
            new_positions = set()
            if isinstance(step, str):
                for x, y in positions:
                    m[x,y].add(step)
                    x, y = MOVES[step](x, y)
                    m[x,y].add(INVERSES[step])
                    new_positions.add((x, y))
            else:
                for option in step:
                    new_positions |= walk_tree(option, positions)
            positions = new_positions
        return positions

    walk_tree(tree, {(0, 0)})

    return m

def part1(s):
    m = contruct_map(s)

    graph = {}
    for (x, y), doors in m.items():
        graph[x,y] = [MOVES[d](x, y)
                      for d in doors]

    answer = lib.graph.longest_path_length(graph, (0, 0))

    print(f'The answer to part one is {answer}')

def part2(s):
    pass

INPUT = lib.aoc.get_input(2018, 20)
part1(INPUT)
part2(INPUT)
