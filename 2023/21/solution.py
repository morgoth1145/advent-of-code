import lib.aoc
import lib.grid

def part1(s):
    grid = lib.grid.FixedGrid.parse(s)

    for coord, c in grid.items():
        if c == 'S':
            start = coord

    positions = [start]

    for i in range(64):
        next_positions = set()

        for p in positions:
            next_positions.update(grid.neighbors(*p))

        positions = [p for p in next_positions
                     if grid[p] != '#']

    answer = len(positions)

    lib.aoc.give_answer(2023, 21, 1, answer)

# BOOKMARK
def part2(s):
    grid = lib.grid.FixedGrid.parse(s)

    for coord, c in grid.items():
        if c == 'S':
            start = coord

    filled = set()
    todo = [start]

    while todo:
        p = todo.pop()
        if p in filled:
            continue
        filled.add(p)

        for n in grid.neighbors(*p):
            if grid[n] == '#':
                continue
            todo.append(n)

    for coord, _ in grid.items():
        if coord not in filled:
            grid[coord] = '#'

##    grid.print('')
##    assert(False)

    even_count, odd_count = 0, 0

    for y in grid.y_range:
        a = grid.x_range[::2]
        b = grid.x_range[1::2]
        if y % 2 == 0:
            even_count += sum(grid[x,y] != '#' for x in b)
            odd_count += sum(grid[x,y] != '#' for x in a)
        else:
            even_count += sum(grid[x,y] != '#' for x in a)
            odd_count += sum(grid[x,y] != '#' for x in b)

    top_endcap = 0
    bottom_endcap = 0

    top_right_endcap = 0
    top_left_endcap = 0
    bot_right_endcap = 0
    bot_left_endcap = 0

    x_range = grid.x_range
    rev_x_range = x_range[::-1]

    overcount = 0

    # BOOKMARK
    for y in grid.y_range:
        a = x_range[::2]
        b = x_range[1::2]

        # Top endcap
        x_span = y-65 # One past the end
        if y % 2 == 0:
            if x_span > 0:
                top_right_endcap += sum(grid[x,y] != '#' for x in x_range[0:x_span:2])
                top_left_endcap += sum(grid[x,y] != '#' for x in rev_x_range[0:x_span:2])
                pass
            x_span += 131
            top_right_endcap += sum(grid[x,y] != '#' for x in x_range[1:x_span:2])
            top_left_endcap += sum(grid[x,y] != '#' for x in rev_x_range[1:x_span:2])
            overcount += sum(grid[x,y] != '#' for x in x_range[1:x_span:2])
            overcount += sum(grid[x,y] != '#' for x in rev_x_range[1:x_span:2])
        else:
            if x_span > 0:
                top_right_endcap += sum(grid[x,y] != '#' for x in x_range[1:x_span:2])
                top_left_endcap += sum(grid[x,y] != '#' for x in rev_x_range[1:x_span:2])
                pass
            x_span += 131
            top_right_endcap += sum(grid[x,y] != '#' for x in x_range[0:x_span:2])
            top_left_endcap += sum(grid[x,y] != '#' for x in rev_x_range[0:x_span:2])
            overcount += sum(grid[x,y] != '#' for x in x_range[0:x_span:2])
            overcount += sum(grid[x,y] != '#' for x in rev_x_range[0:x_span:2])

        # Bottom endcap
        x_span = 65-y # One past the end
        if y % 2 == 0:
            if x_span > 0:
                bot_right_endcap += sum(grid[x,y] != '#' for x in x_range[0:x_span:2])
                bot_left_endcap += sum(grid[x,y] != '#' for x in rev_x_range[0:x_span:2])
            x_span += 131
            bot_right_endcap += sum(grid[x,y] != '#' for x in x_range[1:x_span:2])
            bot_left_endcap += sum(grid[x,y] != '#' for x in rev_x_range[1:x_span:2])
            overcount += sum(grid[x,y] != '#' for x in x_range[1:x_span:2])
            overcount += sum(grid[x,y] != '#' for x in rev_x_range[1:x_span:2])
        else:
            if x_span > 0:
                bot_right_endcap += sum(grid[x,y] != '#' for x in x_range[1:x_span:2])
                bot_left_endcap += sum(grid[x,y] != '#' for x in rev_x_range[1:x_span:2])
            x_span += 131
            bot_right_endcap += sum(grid[x,y] != '#' for x in x_range[0:x_span:2])
            bot_left_endcap += sum(grid[x,y] != '#' for x in rev_x_range[0:x_span:2])
            overcount += sum(grid[x,y] != '#' for x in x_range[0:x_span:2])
            overcount += sum(grid[x,y] != '#' for x in rev_x_range[0:x_span:2])

    top_endcap = top_right_endcap + top_left_endcap
    bottom_endcap = bot_right_endcap + bot_left_endcap

    print(even_count, odd_count)
    print(top_endcap, bottom_endcap)
    print('top right endcap', top_right_endcap)
    print('top left endcap', top_left_endcap)
    print('bot right endcap', bot_right_endcap)
    print('bot left endcap', bot_left_endcap)



    d = grid.width
    time_to_corner = sum(start)
    print(time_to_corner)

    STEPS = 26501365
##    STEPS = 65+131*2

    rem = STEPS % d
    times = STEPS // d
    print(rem, times)

    assert(times % 2 == 0)




    num_caps = 0
    odds = 0
    evens = 0

    for x in range(-times, times+1):
        y_d = times - abs(x)
        if y_d > 0:
            height = y_d * 2 + 1
            if x != 0:
                # Symmetric
                # One cap per row (handles both sides)
                num_caps += 1
            height -= 2
            evens += height // 2
            odds += height // 2 + 1

    print()
    print(evens, odds, num_caps)

    left, right, top, bottom = 0, 0, 0, 0

    for y in grid.y_range:
        x_span = grid.width-abs(y-65) # One past the end
        if y % 2 == 0:
            right += sum(grid[x,y] != '#' for x in x_range[1:x_span:2])
            left += sum(grid[x,y] != '#' for x in rev_x_range[1:x_span:2])
        else:
            right += sum(grid[x,y] != '#' for x in x_range[0:x_span:2])
            left += sum(grid[x,y] != '#' for x in rev_x_range[0:x_span:2])

    y_range = grid.y_range
    rev_y_range = y_range[::-1]

    for x in grid.x_range:
        y_span = grid.height-abs(x-65) # One past the end
        if x % 2 == 0:
            top += sum(grid[x,y] != '#' for y in rev_y_range[1:y_span:2])
            bottom += sum(grid[x,y] != '#' for y in y_range[1:y_span:2])
        else:
            top += sum(grid[x,y] != '#' for y in rev_y_range[0:y_span:2])
            bottom += sum(grid[x,y] != '#' for y in y_range[0:y_span:2])

    print(top, bottom)
    print(left, right)

    print()
    print(top_endcap, bottom_endcap)

    answer = 0
    answer += evens * even_count
    answer += odds * odd_count
    answer += (num_caps // 2) * top_endcap
    answer += (num_caps // 2) * bottom_endcap
    answer += top
    answer += bottom
    answer += left
    answer += right
    answer += top_endcap + bottom_endcap - overcount

##    print()
##    print('Answer?', answer)
##    print('Should be 92811')
##    assert(False)

    lib.aoc.give_answer(2023, 21, 2, answer)






##    print()
##    print()
##    print()
##    assert(start == (65,65))
##    assert(grid.width == grid.height == 131)
##
##    print(start)
##    print(grid.width, grid.height)
##    assert(start[0]*2+1 == grid.width)
##    assert(start[1]*2+1 == grid.height)
##    assert(all(grid[x,start[1]] != '#'
##               for x in grid.x_range))
##    assert(all(grid[start[0],y] != '#'
##               for y in grid.y_range))
##    assert(all(grid[x,0] != '#'
##               for x in grid.x_range))
##    assert(all(grid[x,grid.height-1] != '#'
##               for x in grid.x_range))
##    assert(all(grid[0,y] != '#'
##               for y in grid.y_range))
##    assert(all(grid[grid.width-1,y] != '#'
##               for y in grid.y_range))
##    assert(grid.width == grid.height)
##
##    assert(False)

# BOOKMARK
def part24(s):
    grid = lib.grid.FixedGrid.parse(s)

    for coord, c in grid.items():
        if c == 'S':
            start = coord

    filled = set()
    todo = [start]

    while todo:
        p = todo.pop()
        if p in filled:
            continue
        filled.add(p)

        for n in grid.neighbors(*p):
            if grid[n] == '#':
                continue
            todo.append(n)

    for coord, _ in grid.items():
        if coord not in filled:
            grid[coord] = '#'

    grid[start] = '.'

    x_range = grid.x_range
    rev_x_range = x_range[::-1]

    # BOOKMARK
    to_fill = []
    for y in grid.y_range:
        a = x_range[::2]
        b = x_range[1::2]

        # Top endcap
        x_span = y-65 # One past the end
        if y % 2 == 0:
            if x_span > 0:
##                top_right_endcap += sum(grid[x,y] != '#' for x in x_range[0:x_span:2])
##                top_left_endcap += sum(grid[x,y] != '#' for x in rev_x_range[0:x_span:2])
                pass
            x_span += 131
##            top_right_endcap += sum(grid[x,y] != '#' for x in x_range[1:x_span:2])
##            top_left_endcap += sum(grid[x,y] != '#' for x in rev_x_range[1:x_span:2])
        else:
            if x_span > 0:
##                top_right_endcap += sum(grid[x,y] != '#' for x in x_range[1:x_span:2])
##                top_left_endcap += sum(grid[x,y] != '#' for x in rev_x_range[1:x_span:2])
                pass
            x_span += 131
##            top_right_endcap += sum(grid[x,y] != '#' for x in x_range[0:x_span:2])
##            top_left_endcap += sum(grid[x,y] != '#' for x in rev_x_range[0:x_span:2])

        # Bottom endcap
        x_span = 65-y # One past the end
        if y % 2 == 0:
            if x_span > 0:
##                bot_right_endcap += sum(grid[x,y] != '#' for x in x_range[0:x_span:2])
                to_fill.extend((x,y) for x in x_range[0:x_span:2])
##                bot_left_endcap += sum(grid[x,y] != '#' for x in rev_x_range[0:x_span:2])
            x_span += 131
##            bot_right_endcap += sum(grid[x,y] != '#' for x in x_range[1:x_span:2])
##            bot_left_endcap += sum(grid[x,y] != '#' for x in rev_x_range[1:x_span:2])
        else:
            if x_span > 0:
##                bot_right_endcap += sum(grid[x,y] != '#' for x in x_range[1:x_span:2])
                to_fill.extend((x,y) for x in x_range[1:x_span:2])
##                bot_left_endcap += sum(grid[x,y] != '#' for x in rev_x_range[1:x_span:2])
            x_span += 131
##            bot_right_endcap += sum(grid[x,y] != '#' for x in x_range[0:x_span:2])
##            bot_left_endcap += sum(grid[x,y] != '#' for x in rev_x_range[0:x_span:2])

    for x,y in to_fill:
        if grid[x,y] != '#':
            grid[x,y] = 'O'

    grid.print('')
    assert(False)

# BOOKMARK
def part24(s):
    grid = lib.grid.FixedGrid.parse(s)

    for coord, c in grid.items():
        if c == 'S':
            start = coord

    positions = [start]

    assert(start == (65,65))
    assert(grid.width == grid.height == 131)

    for i in range(65+131*2):
        next_positions = set()

        for x,y in positions:
            for n in [(x-1,y),
                      (x+1,y),
                      (x,y-1),
                      (x,y+1)]:
                next_positions.add(n)

        positions = [(nx,ny) for nx,ny in next_positions
                     if grid[nx%grid.width, ny%grid.height] != '#']

    positions = set(positions)
    print(len(positions))

    # BOOKMARK
    grid[start] = '.'
    for (x,y), _ in grid.items():
        p = (x+131*2,y+131*0)
        if p in positions:
            grid[x,y] = 'O'

    grid.print('')
    print(grid.as_str('').count('O'))

    handled = set()

    top = 0
    bottom = 0
    left = 0
    right = 0

    for x,y in positions:
        if 0 > y >= -grid.height:
            if x < 0 or x >= grid.width:
                handled.add((x,y)) # Top endcaps
                continue
        if grid.height <= y < 2*grid.height:
            if x < 0 or x >= grid.width:
                handled.add((x,y)) # Bottom endcaps
                continue

        if -grid.height > y:
            if 0 <= x < grid.width:
                top += 1
                handled.add((x,y))
                continue

        if 2*grid.height <= y:
            if 0 <= x < grid.width:
                bottom += 1
                handled.add((x,y))
                continue

        if -grid.width > x:
            if 0 <= y < grid.height:
                left += 1
                handled.add((x,y))
                continue

        if 2*grid.width <= x:
            if 0 <= y < grid.height:
                right += 1
                handled.add((x,y))
                continue

        d = abs(x // 131) + abs(y // 131)
        if d >= 2:
            print(x, y, d)
        assert(d < 2)

    print('top', top)
    print('bottom', bottom)
    print('left', left)
    print('right', right)

    unhandled = sorted(positions - handled)
    print(len(handled), len(unhandled))
    if unhandled:
        print('unhandled', unhandled[0])
    assert(False)

    top, bottom, right, left = 0, 0, 0, 0

##    for x,y in positions:
##        if 0 > y >= -grid.height:
##            if x < 0 or x >= grid.width:
##                top_endcap += 1
##        if grid.height <= y < 2*grid.height:
##            if x < 0 or x >= grid.width:
##                bottom_endcap += 1
##
##        if grid.height <= y < 2*grid.height:
##            if grid.width <= x:
##                bot_right_endcap += 1
##            if 0 > x:
##                bot_left_endcap += 1
##        if 0 > y >= -grid.height:
##            if grid.width <= x:
##                top_right_endcap += 1
##            if 0 > x:
##                top_left_endcap += 1
##
##    assert(top_endcap == top_right_endcap + top_left_endcap)
##    assert(bottom_endcap == bot_right_endcap + bot_left_endcap)
##
##    print(top_endcap, bottom_endcap)
##    print('top right endcap', top_right_endcap)
##    print('top left endcap', top_left_endcap)
##    print('bot right endcap', bot_right_endcap)
##    print('bot left endcap', bot_left_endcap)

##    top_endcap = 0
##    bottom_endcap = 0
##    top_right_endcap = 0
##    top_left_endcap = 0
##    bot_right_endcap = 0
##    bot_left_endcap = 0
##
    for x,y in positions:
        if 0 > y >= -grid.height:
            if x < 0 or x >= grid.width:
                top_endcap += 1
        if grid.height <= y < 2*grid.height:
            if x < 0 or x >= grid.width:
                bottom_endcap += 1

        if grid.height <= y < 2*grid.height:
            if grid.width <= x:
                bot_right_endcap += 1
            if 0 > x:
                bot_left_endcap += 1
        if 0 > y >= -grid.height:
            if grid.width <= x:
                top_right_endcap += 1
            if 0 > x:
                top_left_endcap += 1
##
##    assert(top_endcap == top_right_endcap + top_left_endcap)
##    assert(bottom_endcap == bot_right_endcap + bot_left_endcap)
##
##    print(top_endcap, bottom_endcap)
##    print('top right endcap', top_right_endcap)
##    print('top left endcap', top_left_endcap)
##    print('bot right endcap', bot_right_endcap)
##    print('bot left endcap', bot_left_endcap)

    # BOOKMARK
    assert(False)

    print('Extremes')
    print(min(x for x,y in positions))
    print(max(x for x,y in positions))
    print(min(y for x,y in positions))
    print(max(y for x,y in positions))
    print()

    print(start)
    print(grid.width, grid.height)
    assert(start[0]*2+1 == grid.width)
    assert(start[1]*2+1 == grid.height)
    assert(all(grid[x,start[1]] != '#'
               for x in grid.x_range))
    assert(all(grid[start[0],y] != '#'
               for y in grid.y_range))
    assert(all(grid[x,0] != '#'
               for x in grid.x_range))
    assert(all(grid[x,grid.height-1] != '#'
               for x in grid.x_range))
    assert(all(grid[0,y] != '#'
               for y in grid.y_range))
    assert(all(grid[grid.width-1,y] != '#'
               for y in grid.y_range))
    assert(grid.width == grid.height)
    d = grid.width
    time_to_corner = sum(start)
    print(time_to_corner)

    STEPS = 26501365

    rem = STEPS % d
    times = STEPS // d
    print(rem, times)

    assert(times % 2 == 0)

    corners = 0
    supercorners = 0
    odds = 0
    evens = 0

    for x in range(-times, times+1):
        y_d = times - abs(x)
        if y_d > 0:
            height = y_d * 2 + 1
            if x != 0:
                corners += 2
            height -= 2
            evens += height // 2
            odds += height // 2 + 1
        if x != 0:
            supercorners += 2

    print(odds, evens, corners, supercorners)

    # 4 types of corners, evenly split
    assert(corners % 4 == 0)
    corners //= 4

    even_count = 0
    odd_count = 0
    top_count = 0
    bottom_count = 0
    left_count = 0
    right_count = 0
    ul_corner = 0
    ur_corner = 0
    bl_corner = 0
    br_corner = 0

    uul, uur, bbl, bbr = 0, 0, 0, 0

    unknown = 0
    for x,y in positions:
        if 0 <= x < grid.width:
            if 0 <= y < grid.height:
                even_count += 1
            elif grid.height <= y < 2*grid.height:
                odd_count += 1
            elif 2*grid.height <= y < 3*grid.height:
                top_count += 1
            elif -grid.height > y >= -2*grid.height:
                bottom_count += 1
            elif 0 > y >= -grid.height:
                pass # Counted as odd
            else:
                assert(False)
        elif grid.width <= x < 2*grid.width:
            if grid.height <= y < 2*grid.height:
                ur_corner += 1
            elif 0 > y >= -grid.height:
                br_corner += 1
            elif 0 <= y < grid.height:
                pass # Counted as odd
            elif -grid.height > y >= -2*grid.height:
                bbr += 1
            elif 2*grid.height <= y < 3*grid.height:
                uur += 1
            else:
                assert(False)
        elif 2*grid.width <= x < 3*grid.width:
            if 0 <= y < grid.height:
                right_count += 1
            else:
                unknown += 1
        elif 0 > x >= -grid.width:
            if grid.height <= y < 2*grid.height:
                ul_corner += 1
            elif 0 > y >= -grid.height:
                bl_corner += 1
            elif 0 <= y < grid.height:
                pass # Counted as odd
            elif -grid.height > y >= -2*grid.height:
                bbl += 1
            elif 2*grid.height <= y < 3*grid.height:
                uul += 1
            else:
                assert(False)
        elif -grid.width > x >= -2*grid.width:
            if 0 <= y < grid.height:
                left_count += 1
            else:
                unknown += 1
        else:
            assert(False)

    print()
    print(even_count, odd_count)
    print(top_count, bottom_count)
    print(left_count, right_count)
    print(ul_corner, ur_corner, bl_corner, br_corner)
    print(uul, uur, bbl, bbr)
    print(unknown)
    print()

    answer = 0
    answer += evens * even_count
    answer += odds * odd_count
    answer += top_count
    answer += bottom_count
    answer += left_count
    answer += right_count
    answer += corners * ul_corner
    answer += corners * ur_corner
    answer += corners * bl_corner
    answer += corners * br_corner

    answer += supercorners * uur
    answer += supercorners * uul
    answer += supercorners * bbr
    answer += supercorners * bbl

    print(f'The answer to part two is {answer}')
    lib.aoc.give_answer(2023, 21, 2, answer)

def part23(s):
    grid = lib.grid.FixedGrid.parse(s)

    for coord, c in grid.items():
        if c == 'S':
            start = coord

    positions = [start]

    for i in range(65+131*3):
        next_positions = set()

        for x,y in positions:
            for nx,ny in [(x-1,y),
                      (x+1,y),
                      (x,y-1),
                      (x,y+1)]:
                next_positions.add((nx,ny))

        positions = [(nx,ny) for nx,ny in next_positions
                     if grid[nx%grid.width, ny%grid.height] != '#']

    grid[start] = '.'
    for p in positions:
        if p in grid:
            grid[p] = 'O'

    grid.print('')
    assert(False)

def part22(s):
    grid = lib.grid.FixedGrid.parse(s)

    for coord, c in grid.items():
        if c == 'S':
            start = coord

    positions = [start]

    print(start)
    print(grid.width, grid.height)
    assert(start[0]*2+1 == grid.width)
    assert(start[1]*2+1 == grid.height)
    assert(all(grid[x,start[1]] != '#'
               for x in grid.x_range))
    assert(all(grid[start[0],y] != '#'
               for y in grid.y_range))
    assert(all(grid[x,0] != '#'
               for x in grid.x_range))
    assert(all(grid[x,grid.height-1] != '#'
               for x in grid.x_range))
    assert(all(grid[0,y] != '#'
               for y in grid.y_range))
    assert(all(grid[grid.width-1,y] != '#'
               for y in grid.y_range))
    assert(grid.width == grid.height)
    d = grid.width
    time_to_corner = sum(start)
    print(time_to_corner)

    STEPS = 26501365

    rem = STEPS % d
    times = STEPS // d
    print(rem, times)

    universes = [(0,0)]

    for _ in range(times//100):
        new = set()
        for x,y in universes:
            new.add((x-1,y))
            new.add((x+1,y))
            new.add((x,y-1))
            new.add((x,y+1))
        universes = list(new)

    print(len(universes))
    assert(False)

    for i in range(50):
        next_positions = set()

        for x,y in positions:
            for nx, ny in [(x-1,y),
                           (x+1,y),
                           (x,y-1),
                           (x,y+1)]:
                next_positions.add((nx,ny))

        positions = [(x,y) for x,y in next_positions
                     if grid[x%grid.width, y%grid.height] != '#']

    answer = len(positions)

    print(f'The answer to part two is {answer}')
    lib.aoc.give_answer(2023, 21, 2, answer)

def part24(s):
    grid = lib.grid.FixedGrid.parse(s)

    for coord, c in grid.items():
        if c == 'S':
            start = coord

    STEPS = 65+131*2
    STEPS = 5000
    known = set()

    positions = [start]

    for i in range(STEPS):
        next_positions = set()

        for x,y in positions:
            next_positions.update([(x-1,y),
                                   (x+1,y),
                                   (x,y-1),
                                   (x,y+1)])

        positions = [(nx,ny) for nx,ny in next_positions - known
                     if grid[nx%grid.width, ny%grid.height] != '#']
        if (STEPS - i) % 2 == 1:
            known.update(positions)

    positions = known

    grid[start] = '.'
    for p, _ in grid.items():
        if p in positions:
            grid[p] = 'O'

##    for x,y in positions:
##        grid[x%grid.width,y%grid.height] = 'O'

    grid.print('')

    print(len(positions))
    assert(False)

INPUT = lib.aoc.get_input(2023, 21)
part1(INPUT)
##INPUT = '''...........
##.....###.#.
##.###.##..#.
##..#.#...#..
##....#.#....
##.##..S####.
##.##..#...#.
##.......##..
##.##.#.####.
##.##..##.##.
##...........'''
part2(INPUT)
