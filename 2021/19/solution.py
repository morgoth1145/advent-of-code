import lib.aoc

ROTATIONS = [
    ((-1, 0, 0), (0, -1, 0), (0, 0, 1)),
    ((-1, 0, 0), (0, 0, -1), (0, -1, 0)),
    ((-1, 0, 0), (0, 0, 1), (0, 1, 0)),
    ((-1, 0, 0), (0, 1, 0), (0, 0, -1)),
    ((0, -1, 0), (-1, 0, 0), (0, 0, -1)),
    ((0, -1, 0), (0, 0, -1), (1, 0, 0)),
    ((0, -1, 0), (0, 0, 1), (-1, 0, 0)),
    ((0, -1, 0), (1, 0, 0), (0, 0, 1)),
    ((0, 0, -1), (-1, 0, 0), (0, 1, 0)),
    ((0, 0, -1), (0, -1, 0), (-1, 0, 0)),
    ((0, 0, -1), (0, 1, 0), (1, 0, 0)),
    ((0, 0, -1), (1, 0, 0), (0, -1, 0)),
    ((0, 0, 1), (-1, 0, 0), (0, -1, 0)),
    ((0, 0, 1), (0, -1, 0), (1, 0, 0)),
    ((0, 0, 1), (0, 1, 0), (-1, 0, 0)),
    ((0, 0, 1), (1, 0, 0), (0, 1, 0)),
    ((0, 1, 0), (-1, 0, 0), (0, 0, 1)),
    ((0, 1, 0), (0, 0, -1), (-1, 0, 0)),
    ((0, 1, 0), (0, 0, 1), (1, 0, 0)),
    ((0, 1, 0), (1, 0, 0), (0, 0, -1)),
    ((1, 0, 0), (0, -1, 0), (0, 0, -1)),
    ((1, 0, 0), (0, 0, -1), (0, 1, 0)),
    ((1, 0, 0), (0, 0, 1), (0, -1, 0)),
    ((1, 0, 0), (0, 1, 0), (0, 0, 1)),
]

class Scanner:
    def __init__(self, num, coords):
        self.num = num
        self.coords = coords

    def print(self):
        print(f'--- scanner {self.num} ---')
        for c in self.coords:
            print(','.join(map(str, c)))

    def gen_alt_orientations(self):
        def do_rotation(xrot, yrot, zrot):
            new_coords = []
            for c in self.coords:
                nx = sum(a*b for a,b in zip(c, xrot))
                ny = sum(a*b for a,b in zip(c, yrot))
                nz = sum(a*b for a,b in zip(c, zrot))
                new_coords.append((nx, ny, nz))
            return Scanner(self.num, new_coords)

        for rot in ROTATIONS:
            yield do_rotation(*rot)

def parse_scans(s):
    groups = s.split('\n\n')
    for idx, scanner in enumerate(groups):
        lines = scanner.splitlines()
        coords = []
        for line in lines[1:]:
            coords.append(tuple(map(int, line.split(','))))
        yield Scanner(idx, set(coords))

def find_scanner_match(known, scanners):
    for s in scanners.values():
        for o in s.gen_alt_orientations():
            test_coords = list(o.coords)
            for idx, base_c in enumerate(known.coords):
                # TODO: Why doesn't this work? Maybe I'm not thinking things through?
##                if idx+11 >= len(known.coords):
##                    # Not enough left to find a match
##                    break
                for idx2, test_c in enumerate(o.coords):
                    if idx2+11 >= len(test_coords):
                        # Not enough left to find a match
                        break
                    xoff, yoff, zoff = (a-b for a, b in zip(base_c, test_c))
                    x,y,z = test_c
                    c = (x+xoff, y+yoff, z+zoff)
                    matches = 1
                    for c in test_coords[idx2+1:]:
                        x,y,z = c
                        c2 = (x+xoff, y+yoff, z+zoff)
                        if c2 in known.coords:
                            matches += 1
                    if matches >= 12:
                        # We match!
                        match_coords = [(x+xoff, y+yoff, z+zoff)
                                        for x,y,z in o.coords]
                        o.coords = set(match_coords)
                        del scanners[s.num]
                        return o
    assert(False)

def part1(s):
    scanners = {scan.num:scan
                for scan in parse_scans(s)}

    known = scanners[0]
    del scanners[0]

    while len(scanners):
        print(len(scanners), 'left')
        match = find_scanner_match(known, scanners)
        known.coords |= match.coords

    answer = len(known.coords)

    print(f'The answer to part one is {answer}')

def part2(s):
    pass

INPUT = lib.aoc.get_input(2021, 19)
part1(INPUT)
part2(INPUT)
