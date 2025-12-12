import collections

import lib.aoc
import lib.grid

def part1(s):
    groups = s.split('\n\n')
    grids = groups[:-1]
    stuff = groups[-1]

    grids2 = []
    for g in grids:
        lines = g.splitlines()
        g = lines[1:]
        grids2.append(lib.grid.FixedGrid.parse('\n'.join(lines[1:])))

    grid_widths = [g.width for g in grids2]
    grid_heights = [g.height for g in grids2]

    assert(set(grid_widths + grid_heights) == {3})

    PRES_DIM = 3

    presents = collections.defaultdict(list)

    for idx, g in enumerate(grids2):
        seen = set()
        for _ in range(4):
            gs = g.as_str()
            if gs not in seen:
                presents[idx].append(g)
                seen.add(gs)

            gp = g.transpose()
            gps = gp.as_str()
            if gps not in seen:
                presents[idx].append(gp)
                seen.add(gps)

            # Rotate TODO
            rot = ''
            for x in g.x_range:
                col = g.col(x)
                rot += ''.join(col[::-1])
                rot += '\n'

            g = lib.grid.FixedGrid.parse(rot.strip())

    stuff2 = []
    for l in stuff.splitlines():
        a, rest = l.split(': ')
        rest = list(map(int, rest.split()))
        a, b = map(int, a.split('x'))
        stuff2.append((a, b, rest))

    answer = 0

    def test_pack_quick(g, present_picks):
        needed = 0
        for pidx, p in enumerate(present_picks):
            per_pres = 0
            pshape = presents[pidx][0]
            for _, c in pshape.items():
                if c == '#':
                    per_pres += 1

            needed += per_pres * p

        return needed <= g.width*g.height

##    def test_pack(g, present_picks):
##        if sum(present_picks) == 0:
##            return True
##
##        for pidx, p in enumerate(present_picks):
##            if p > 0:
##                present_picks[pidx] -= 1
##
##                # Put in g
##
##                ans = test_pack(g, present_picks)
##                present_picks[pidx] += 1
##                if ans:
##                    return True
##
##        return False

    test_pack = test_pack_quick

    for w, h, picks in stuff2:
        grid = '\n'.join(['.' * w]*h)
        g = lib.grid.FixedGrid.parse(grid)

        if test_pack(g, picks):
            answer += 1

    lib.aoc.give_answer(2025, 12, 1, answer)

def part2(s):
    print('There is no part 2 on day 12!')

INPUT = lib.aoc.get_input(2025, 12)
part1(INPUT)
part2(INPUT)
