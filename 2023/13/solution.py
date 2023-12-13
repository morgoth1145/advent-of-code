import lib.aoc
import lib.grid

def parse_input(s):
    for group in s.split('\n\n'):
        yield lib.grid.FixedGrid.parse(group)

def find_reflection(grid):
    verts = []
    for i in range(1, grid.width):
        left = []
        right = []
        for j in range(i-1, -1, -1):
            left.append(grid.col(j))
        for j in range(i, grid.width):
            right.append(grid.col(j))
        n = min(len(left), len(right))
        left = left[:n]
        right = right[:n]
        if left == right:
            verts.append(i)

    horizontals = []
    for i in range(1, grid.height):
        top = []
        bottom = []
        for j in range(i-1, -1, -1):
            top.append(grid.row(j))
        for j in range(i, grid.height):
            bottom.append(grid.row(j))
        n = min(len(top), len(bottom))
        top = top[:n]
        bottom = bottom[:n]
        if top == bottom:
            horizontals.append(i)

    return verts, horizontals

def part1(s):
    data = list(parse_input(s))

    answer = 0

    for g in data:
        vert, horiz = find_reflection(g)
        if len(vert) == 1:
            assert(len(horiz) == 0)
            answer += vert[0]
        else:
            assert(len(vert) == 0)
            assert(len(horiz) == 1)
            answer += horiz[0] * 100

    lib.aoc.give_answer(2023, 13, 1, answer)

def part2(s):
    pass

INPUT = lib.aoc.get_input(2023, 13)
part1(INPUT)
part2(INPUT)
