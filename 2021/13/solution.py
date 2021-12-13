import lib.aoc
import lib.ocr

def parse(s):
    groups = s.split('\n\n')

    pairs = {tuple(map(int, line.split(',')))
             for line in groups[0].splitlines()}
    folds = []
    for line in groups[1].splitlines():
        axis, n = line.split()[2].split('=')
        folds.append((axis, int(n)))

    return pairs, folds

def do_fold(dots, fold):
    axis, n = fold

    def reflect(c):
        assert(c != n)
        return min(c, 2*n-c)

    if axis == 'x':
        return {(reflect(x), y)
                for x, y in dots}
    elif axis == 'y':
        return {(x, reflect(y))
                for x, y in dots}

def part1(s):
    dots, folds = parse(s)

    dots = do_fold(dots, folds[0])

    answer = len(dots)

    print(f'The answer to part one is {answer}')

def part2(s):
    dots, folds = parse(s)

    for fold in folds:
        dots = do_fold(dots, fold)

    answer = lib.ocr.parse_coord_set(dots)

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2021, 13)
part1(INPUT)
part2(INPUT)
