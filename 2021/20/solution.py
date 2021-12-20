import lib.aoc
import lib.grid

def parse_input(s):
    algo, image = s.split('\n\n')
    image = lib.grid.FixedGrid.parse(image)
    return algo, image.to_dict(), image.width, image.height

def neighbors(x, y):
    for ay in (-1, 0, 1):
        for ax in (-1, 0, 1):
            yield (x+ax, y+ay)

def step(algo, image, xrange, yrange, default):
    new_im = {}
    xrange = range(xrange[0]-1, xrange[-1]+2)
    yrange = range(yrange[0]-1, yrange[-1]+2)
    for x in xrange:
        for y in yrange:
            section = [image.get(n, default)
                       for n in neighbors(x,y)]
            section = ''.join(section)
            section = section.replace('.', '0')
            section = section.replace('#', '1')
            idx = int(section, 2)
            new_im[x,y] = algo[idx]

    # Figure out new out of bounds default
    section = (default*9).replace('.', '0').replace('#', '1')
    default = algo[int(section, 2)]

    return new_im, xrange, yrange, default

def part1(s):
    algo, image, width, height = parse_input(s)
    xrange = range(width)
    yrange = range(height)

    default = '.'

    for _ in range(2):
        image, xrange, yrange, default = step(algo, image, xrange, yrange, default)

    answer = sum(1 for c in image.values() if c == '#')

    print(f'The answer to part one is {answer}')

def part2(s):
    algo, image, width, height = parse_input(s)
    xrange = range(width)
    yrange = range(height)

    default = '.'

    for _ in range(50):
        image, xrange, yrange, default = step(algo, image, xrange, yrange, default)

    answer = sum(1 for c in image.values() if c == '#')

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2021, 20)
part1(INPUT)
part2(INPUT)
