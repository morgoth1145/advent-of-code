import lib.aoc
import lib.grid

def solve(s):
    grid = lib.grid.FixedGrid.parse(s)

    pos = None

    for x in range(grid.width):
        if grid[x,0] == '|':
            pos = (x,0)
            break

    assert(pos is not None)
    x, y = pos
    dx, dy = 0, 1

    seen_letters = ''
    steps = 1 # Count the first step onto the board

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

        steps += 1

        if val not in '-|+':
            # Letter, accumulate it
            seen_letters += val

    return seen_letters, steps

def part1(s):
    answer, _ = solve(s)

    lib.aoc.give_answer(2017, 19, 1, answer)

def part2(s):
    _, answer = solve(s)

    lib.aoc.give_answer(2017, 19, 2, answer)

INPUT = lib.aoc.get_input(2017, 19)
part1(INPUT)
part2(INPUT)
