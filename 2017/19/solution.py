import lib.aoc
import lib.grid

def part1(s):
    grid = lib.grid.FixedGrid.parse(s)

    pos = None

    for x in range(grid.width):
        if grid[x,0] == '|':
            pos = (x,0)
            break

    assert(pos is not None)
    x, y = pos
    dx, dy = 0, 1

    answer = ''

    while True:
        cur = grid[x,y]
        if cur == '+':
            nx, ny = x+dx, y+dy
            if grid[nx,ny] not in '-|':
                # Forced turn
                good_turn = False
                for cand in [(dy, dx),
                             (-dy, -dx)]:
                    dx, dy = cand
                    nx, ny = x+dx, y+dy
                    if grid[nx,ny] != ' ':
                        good_turn = True
                        break
                assert(good_turn)
                continue

        x, y = x+dx, y+dy
        val = grid[x,y]
        if val == ' ':
            # Reached the end
            break

        if val not in '-|+':
            # Letter, accumulate it
            answer += val

    print(f'The answer to part one is {answer}')

def part2(s):
    pass

INPUT = lib.aoc.get_input(2017, 19)
part1(INPUT)
part2(INPUT)
