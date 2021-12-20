import lib.aoc
import lib.grid

def run(s, num_steps):
    s = s.translate(str.maketrans('.#', '01'))

    algo, im = s.split('\n\n')
    im = lib.grid.FixedGrid.parse(im)
    xrange = range(im.width)
    yrange = range(im.height)
    im = im.to_dict()

    # The infinite void starts out off
    default = '0'

    for _ in range(num_steps):
        new_im = {}

        xrange = range(xrange[0]-1, xrange[-1]+2)
        yrange = range(yrange[0]-1, yrange[-1]+2)
        for x in xrange:
            for y in yrange:
                idx = ''.join(im.get((x+dx, y+dy), default)
                              for dy in (-1, 0, 1)
                              for dx in (-1, 0, 1))
                idx = int(idx, 2)
                new_im[x,y] = algo[idx]

        # Figure out new out of bounds default
        default = algo[int(default * 9, 2)]

        im = new_im

    # Not exercised in the problem, but I want to handle it anyway
    if default == '1':
        return 'infinity'

    return sum(map(int, im.values()))

def part1(s):
    answer = run(s, 2)
    print(f'The answer to part one is {answer}')

def part2(s):
    answer = run(s, 50)
    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2021, 20)
part1(INPUT)
part2(INPUT)
