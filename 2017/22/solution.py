import lib.aoc
import lib.grid

def part1(s):
    grid = lib.grid.FixedGrid.parse(s)

    x, y = (grid.width)//2, (grid.height)//2
    d = grid.to_dict()

    dx, dy = 0, -1

    answer = 0

    for step in range(10000):
        if d.get((x,y), '.') == '.':
            dx, dy = dy, -dx # Turn left
            d[x,y] = '#'
            answer += 1
        else:
            dx, dy = -dy, dx  # Turn right
            d[x,y] = '.'

        x += dx
        y += dy

    lib.aoc.give_answer(2017, 22, 1, answer)

def part2(s):
    grid = lib.grid.FixedGrid.parse(s)

    x, y = (grid.width)//2, (grid.height)//2
    d = grid.to_dict()

    dx, dy = 0, -1

    answer = 0

    for step in range(10000000):
        state = d.get((x,y), '.')
        if state == '.': # Clean
            dx, dy = dy, -dx # Turn left
        elif state == 'W':
            pass
        elif state == '#': # Infected
            dx, dy = -dy, dx # Turn right
        elif state == 'F':
            dx, dy = -dx, -dy
        else:
            assert(False)

        if state == '.': # Clean
            d[x,y] = 'W'
        elif state == 'W':
            d[x,y] = '#'
            answer += 1
        elif state == '#': # Infected
            d[x,y] = 'F'
        elif state == 'F':
            d[x,y] = '.'
        else:
            assert(False)

        x += dx
        y += dy

    lib.aoc.give_answer(2017, 22, 2, answer)

INPUT = lib.aoc.get_input(2017, 22)
part1(INPUT)
part2(INPUT)
