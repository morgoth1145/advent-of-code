import lib.aoc

ROCKS = [
    [(2, 0), (3, 0), (4, 0), (5, 0)], # Horizontal Line
    [(3, 0), (2, 1), (3, 1), (4, 1), (3, 2)], # Plus
    [(2, 0), (3, 0), (4, 0), (4, 1), (4, 2)], # L
    [(2, 0), (2, 1), (2, 2), (2, 3)], # Vertical Bar
    [(2, 0), (2, 1), (3, 0), (3, 1)], # Square
]

def part1(s):
    WIDTH = 7

    tower = {(x, 0) for x in range(WIDTH)}

    jet_idx = 0

    for rock_idx in range(2022):
        rock = ROCKS[rock_idx % len(ROCKS)]
        y_off = max(y for x,y in tower) + 4
        rock = [(x, y+y_off) for x, y in rock]

        while True:
            jet = s[jet_idx % len(s)]
            if jet == '<':
                dx = -1
            else:
                dx = 1
            jet_idx += 1
            new_rock = [(x+dx, y) for x, y in rock]
            if any(x < 0 or x >= WIDTH for x, y in new_rock):
                new_rock = rock
            elif any(c in tower for c in new_rock):
                new_rock = rock
            rock = new_rock
            new_rock = [(x, y-1) for x,y in rock]
            if any(c in tower for c in new_rock):
                # It settled
                tower.update(rock)
                break

            rock = new_rock

    answer = max(y for x,y in tower)

    lib.aoc.give_answer(2022, 17, 1, answer)

def part2(s):
    pass

INPUT = lib.aoc.get_input(2022, 17)
part1(INPUT)
part2(INPUT)
