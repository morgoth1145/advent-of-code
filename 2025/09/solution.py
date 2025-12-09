import lib.aoc

def part1(s):
    vertices = [tuple(map(int, l.split(',')))
                for l in s.splitlines()]

    answer = max((abs(x-x2)+1) * (abs(y-y2)+1)
                 for idx, (x, y) in enumerate(vertices)
                 for x2, y2 in vertices[idx+1:])

    lib.aoc.give_answer(2025, 9, 1, answer)

def part2(s):
    vertices = [tuple(map(int, l.split(',')))
                for l in s.splitlines()]

    edges = [(min(c, c2), max(c, c2))
             for c, c2
             in zip(vertices, vertices[1:] + vertices[:1])]

    def is_valid_rect(x, y, x2, y2):
        x, x2 = sorted([x, x2])
        y, y2 = sorted([y, y2])

        if any(edge_x2 > x and edge_x < x2 and
               edge_y2 > y and edge_y < y2
               for (edge_x, edge_y), (edge_x2, edge_y2)
               in edges):
            # An edge intersects the rectangle, this rectangle is invalid
            return False

        return True

    answer = 0

    for idx, (x, y) in enumerate(vertices):
        for x2, y2 in vertices[idx+1:]:
            area = (abs(x-x2)+1) * (abs(y-y2)+1)

            if area <= answer:
                continue # Don't bother testing if it's smaller

            if not is_valid_rect(x, y, x2, y2):
                continue

            answer = area

    lib.aoc.give_answer(2025, 9, 2, answer)

INPUT = lib.aoc.get_input(2025, 9)
part1(INPUT)
part2(INPUT)
