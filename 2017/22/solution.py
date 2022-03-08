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

    print(f'The answer to part one is {answer}')

def part2(s):
    pass

INPUT = lib.aoc.get_input(2017, 22)
part1(INPUT)
part2(INPUT)
