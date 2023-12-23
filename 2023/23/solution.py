import lib.aoc
import lib.grid

def part1(s):
    grid = lib.grid.FixedGrid.parse(s)

    end_y = grid.height-1
    for x in grid.x_range:
        if grid[x,0] == '.':
            start = x,0
        if grid[x,end_y] == '.':
            end = x,end_y

    answer = 0
    best = None

    paths = [((start,),0)]

    while paths:
        new_paths = set()

        for p, d in paths:
            coord = p[-1]
            c = grid[coord]
            if c in '<>v^':
                x,y = coord
                if c == '<':
                    n = (x-1,y)
                elif c == '>':
                    n = (x+1,y)
                elif c == '^':
                    n = (x,y-1)
                elif c == 'v':
                    n = (x,y+1)
                if n not in p:
                    new_paths.add((p + (n,), d+1))
                continue
            else:
                assert(c == '.')
            for n in grid.neighbors(*coord):
                if n in p:
                    continue
                if n == end:
                    dist = d+1
                    if dist > answer:
                        answer = dist
                        best = p + (n,)
                    continue
                if grid[n] == '#':
                    continue
                new_paths.add((p + (n,), d+1))

        paths = new_paths

    lib.aoc.give_answer(2023, 23, 1, answer)

def part2(s):
    pass

INPUT = lib.aoc.get_input(2023, 23)
part1(INPUT)
part2(INPUT)
