import lib.aoc
import lib.grid

def parse(s):
    groups = s.split('\n\n')

    pairs = []
    for line in groups[0].splitlines():
        pairs.append(tuple(map(int, line.split(','))))

    folds = []
    for line in groups[1].splitlines():
        assert(line.startswith('fold along '))
        rest = line[len('fold along '):]
        axis, n = rest.split('=')
        folds.append((axis, int(n)))

    return pairs, folds

def do_fold(dots, fold):
    axis, n = fold

    if axis == 'x':
        new_dots = set()
        for x, y in dots:
            if x < n:
                new_dots.add((x, y))
            else:
                assert(x > n)
                diff = x-n
                new_x = n-diff
                new_dots.add((new_x, y))
        return new_dots
    elif axis == 'y':
        new_dots = set()
        for x, y in dots:
            if y < n:
                new_dots.add((x, y))
            else:
                assert(y > n)
                diff = y-n
                new_y = n-diff
                new_dots.add((x, new_y))
        return new_dots
    else:
        assert(False)

def part1(s):
    pairs, folds = parse(s)

    dots = set()
    for x, y in pairs:
        dots.add((x,y))

    dots = do_fold(dots, folds[0])

    answer = len(dots)

    print(f'The answer to part one is {answer}')

def part2(s):
    pairs, folds = parse(s)

    dots = set()
    for x, y in pairs:
        dots.add((x,y))

    for fold in folds:
        dots = do_fold(dots, fold)

    dots = {c:'#' for c in dots}

    grid = lib.grid.FixedGrid.from_dict(dots, missing='.')
    grid.print('')

    answer = input('What are the letters? ')

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2021, 13)
part1(INPUT)
part2(INPUT)
