def to_dict(grid):
    '''Converts a list of list based grid to a coordinate->value dictionary.
    Expects the grid to be subscripted by x then y.
    '''
    return {(x,y):val
            for x,col in enumerate(grid)
            for y,val in enumerate(col)}

def transpose(grid):
    '''Transposes the list of list based grid.
    '''
    width = len(grid)
    height = len(grid[0])
    new_grid = [[grid[x][y]
                 for x in range(width)]
                for y in range(height)]
    return new_grid

def pretty_print(grid, spacing=' '):
    '''Prints out the list of list based grid on screen for analysis.
    '''
    width = len(grid)
    height = len(grid[0])
    print('\n'.join(spacing.join(str(grid[x][y])
                                 for x in range(width))
                    for y in range(height)))

def from_dict(d):
    '''Converts a coordinate->value dictionary to a list of list based grid.
    The converted grid will be subscripted by x then y.
    '''
    x_domain = set()
    y_domain = set()
    for x,y in d.keys():
        x_domain.add(x)
        y_domain.add(y)
    x_domain = sorted(x_domain)
    y_domain = sorted(y_domain)
    assert(x_domain[0] == 0 and x_domain[-1] == len(x_domain)-1)
    assert(y_domain[0] == 0 and y_domain[-1] == len(y_domain)-1)
    assert(len(x_domain) * len(y_domain) == len(d))

    return [[d[x,y]
             for y in y_domain]
            for x in x_domain]
