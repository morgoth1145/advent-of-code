import itertools

# TODO: Should FixedGrid allow offset domains (say -1->4 for x and 3->8 for y)?
class FixedGrid:
    '''Fixed size grid utility class to simplify grid operations and minimize
    bugs.
    '''
    def __init__(self, grid):
        self._grid = grid
        self._width = len(self._grid)
        self._height = len(self._grid[0])

    @staticmethod
    def parse(s, linesplit_fn=None, line_separator='\n', value_fn=None):
        grid = []
        for line in s.split(line_separator):
            if linesplit_fn is not None:
                line = linesplit_fn(line)
            if value_fn is None:
                grid.append(list(line))
            else:
                grid.append(list(map(value_fn, line)))
        return FixedGrid(grid).transpose()

    @staticmethod
    def from_dict(d, missing=None):
        '''Converts a coordinate->value dictionary to a FixedGrid.
        Expects that minimum x and y coordinates in the grid are both 0.

        Arguments:
        missing -- Value to use for any coordinates not present in the dictionary
        '''
        low_x, high_x = None, None
        low_y, high_y = None, None
        for x, y in d.keys():
            if low_x is None:
                low_x, high_x = x, x
                low_y, high_y = y, y
            else:
                low_x = min(low_x, x)
                high_x = max(high_x, x)
                low_y = min(low_y, y)
                high_y = max(high_y, y)

        assert(low_x == low_y == 0)

        return FixedGrid([[d.get((x, y), missing)
                           for y in range(low_y, high_y+1)]
                          for x in range(low_x, high_x+1)])

    def to_dict(self):
        return {(x,y): val
                for x,col in enumerate(self._grid)
                for y,val in enumerate(col)}

    def transpose(self):
        return FixedGrid([[self._grid[x][y]
                           for x in range(self._width)]
                          for y in range(self._height)])

    @property
    def width(self):
        return self._width

    @property
    def x_range(self):
        return range(self.width)

    @property
    def height(self):
        return self._height

    @property
    def y_range(self):
        return range(self._height)

    @property
    def area(self):
        return self._width * self._height

    def __contains__(self, c):
        x, y = c
        return 0 <= x < self._width and 0 <= y < self._height

    def __getitem__(self, c):
        x, y = c
        assert(0 <= x < self._width and 0 <= y < self._height)
        return self._grid[x][y]

    def __setitem__(self, c, val):
        x, y = c
        assert(0 <= x < self._width and 0 <= y < self._height)
        self._grid[x][y] = val

    def row(self, y):
        return [self._grid[x][y] for x in self.x_range]

    def col(self, x):
        return self._grid[x][:]

    def items(self, column_first = False):
        '''Generates all coordinate,value pairs in the grid for iteration.

        Arguments:
        column_first -- Iterate by column first rather than by row first
        '''
        if column_first:
            for y in range(self._height):
                for x, col in enumerate(self._grid):
                    yield (x, y), col[y]
        else:
            for x, col in enumerate(self._grid):
                for y, val in enumerate(col):
                    yield (x, y), val

    def neighbors(self, x, y, diagonals=False):
        assert(0 <= x < self._width and 0 <= y < self._height)
        if diagonals:
            for nx, ny in itertools.product((x-1, x, x+1),
                                            (y-1, y, y+1)):
                if x == nx and y == ny:
                    continue
                if 0 <= nx < self._width and 0 <= ny < self._height:
                    yield nx, ny
        else:
            if 0 < x:
                yield x-1, y
            if x+1 < self._width:
                yield x+1, y
            if 0 < y:
                yield x, y-1
            if y+1 < self._height:
                yield x, y+1

    def print(self, line_spacing=' '):
        print(self.as_str(line_spacing))

    def as_str(self, line_spacing=' '):
        return '\n'.join(line_spacing.join(str(self._grid[x][y])
                                           for x in range(self._width))
                         for y in range(self._height))

# TODO: ExpandingGrid (probably dict-based)
