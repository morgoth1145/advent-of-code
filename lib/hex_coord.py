import typing

_NS_MOVES = [
    ('ne', 1, 1),
    ('n', 0, 2),
    ('nw', -1, 1),
    ('sw', -1, -1),
    ('s', 0, -2),
    ('se', 1, -1),
]

class NSHexCoord(typing.NamedTuple):
    '''Hex coordinate on a North-South dominant grid. (That is, it contains
    North and South neighbors in addition to ne, se, nw, and sw.)
    '''
    x: int = 0
    y: int = 0

    def move(self, d):
        return getattr(self, d)

    @property
    def neighbors(self):
        for _, dx, dy in _NS_MOVES:
            yield NSHexCoord(self.x + dx, self.y + dy)

    def moves_to_reach(self, other):
        assert(isinstance(other, NSHexCoord))

        x_dist = other.x - self.x
        y_dist = other.y - self.y

        dx = 1 if x_dist > 0 else -1
        xdir = 'e' if x_dist > 0 else 'w'
        while x_dist != 0:
            if y_dist > 0:
                yield f'n{xdir}'
                y_dist -= 1
            else:
                yield f's{xdir}'
                y_dist += 1
            x_dist -= dx

        dy = 2 if y_dist > 0 else -2
        ydir = 'n' if y_dist > 0 else 's'
        while y_dist != 0:
            yield ydir
            y_dist -= dy

    def steps_to(self, other):
        assert(isinstance(other, NSHexCoord))
        x_dist = abs(self.x - other.x)
        y_dist = abs(self.y - other.y)
        if x_dist > y_dist:
            # We have to zig-zag to the destination
            return x_dist
        # x moves get us most of the way on the y direction, then we can
        # move 2 at a time
        return x_dist + (y_dist - x_dist) // 2

# Moves as properties
def _make_ns_hex_move_getter(dx, dy):
    return lambda self: NSHexCoord(self.x + dx, self.y + dy)

for d, dx, dy in _NS_MOVES:
    setattr(NSHexCoord, d, property(_make_ns_hex_move_getter(dx, dy)))

_EW_MOVES = [
    ('se', 1, -1),
    ('e', 2, 0),
    ('ne', 1, 1),
    ('nw', -1, 1),
    ('w', -2, 0),
    ('sw', -1, -1),
]

class EWHexCoord(typing.NamedTuple):
    '''Hex coordinate on a East-West dominant grid. (That is, it contains
    East and West neighbors in addition to ne, se, nw, and sw.)
    '''
    x: int = 0
    y: int = 0

    def move(self, d):
        return getattr(self, d)

    @property
    def neighbors(self):
        for _, dx, dy in _EW_MOVES:
            yield EWHexCoord(self.x + dx, self.y + dy)

    def moves_to_reach(self, other):
        assert(isinstance(other, EWHexCoord))

        x_dist = other.x - self.x
        y_dist = other.y - self.y

        dy = 1 if y_dist > 0 else -1
        ydir = 'n' if y_dist > 0 else 's'
        while y_dist != 0:
            if x_dist > 0:
                yield f'{ydir}e'
                x_dist -= 1
            else:
                yield f'{ydir}w'
                x_dist += 1
            y_dist -= dy

        dx = 2 if x_dist > 0 else -2
        xdir = 'e' if x_dist > 0 else 'w'
        while x_dist != 0:
            yield xdir
            x_dist -= dx

    def steps_to(self, other):
        assert(isinstance(other, EWHexCoord))
        x_dist = abs(self.x - other.x)
        y_dist = abs(self.y - other.y)
        if y_dist > x_dist:
            # We have to zig-zag to the destination
            return y_dist
        # y moves get us most of the way on the x direction, then we can
        # move 2 at a time
        return y_dist + (x_dist - y_dist) // 2

# Moves as properties
def _make_ew_hex_move_getter(dx, dy):
    return lambda self: EWHexCoord(self.x + dx, self.y + dy)

for d, dx, dy in _EW_MOVES:
    setattr(EWHexCoord, d, property(_make_ew_hex_move_getter(dx, dy)))
