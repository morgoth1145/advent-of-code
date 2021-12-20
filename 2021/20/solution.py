import lib.aoc
import lib.grid

def run(s, iterations):
    s = s.translate(str.maketrans('.#', '01'))

    algo, im = s.split('\n\n')

    if algo[0] == '1' == algo[511]:
        # Once the infinite void turns on it stays on! Oh no!
        if iterations > 0:
            return 'infinity'
        # We must not be running any iterations...carry on
    elif algo[0] == '1' and algo[511] == '0':
        # The infinite void blinks. If we run an odd number of iterations
        # then it'll be on and we'll have an infinite number of lights on!
        if iterations % 2 == 1:
            return 'infinity'

    im = lib.grid.FixedGrid.parse(im)
    xrange = range(im.width)
    yrange = range(im.height)
    im = im.to_dict()

    # The infinite void starts out off
    default = '0'

    for _ in range(iterations):
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

    assert(default == '0')

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
