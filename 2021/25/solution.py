import lib.aoc
import lib.grid

def step(eastward, southward, width, height):
    moved = False

    new_east = set()
    for x,y in eastward:
        new_c = ((x+1) % width, y)
        if new_c in eastward or new_c in southward:
            # Can't move
            new_east.add((x,y))
        else:
            new_east.add(new_c)
            moved = True

    eastward = new_east

    new_south = set()
    for x,y in southward:
        new_c = (x, (y + 1) % height)
        if new_c in eastward or new_c in southward:
            # Can't move
            new_south.add((x,y))
        else:
            new_south.add(new_c)
            moved = True

    southward = new_south

    return eastward, southward, moved

def part1(s):
    grid = lib.grid.FixedGrid.parse(s)

    eastward = {c for c,v in grid.items() if v == '>'}
    southward = {c for c,v in grid.items() if v == 'v'}
    width = grid.width
    height = grid.height

    answer = 0
    while True:
        answer += 1
        eastward, southward, moved = step(eastward, southward, width, height)

        if not moved:
            break

    lib.aoc.give_answer(2021, 25, 1, answer)

def part2(s):
    print('There is no part two for Christmas!')

INPUT = lib.aoc.get_input(2021, 25)
part1(INPUT)
part2(INPUT)
