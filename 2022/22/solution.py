import collections
import math

import lib.aoc
import lib.graphics

def parse_path(path):
    step = ''

    for c in path:
        if c in 'LR':
            if step != '':
                yield int(step), c
                step = ''
            else:
                yield 0, c
        else:
            step += c

    if len(step):
        yield int(step), ''

def solve(s, wrap_fn_factory):
    grid, path = s.split('\n\n')
    grid_lines = grid.splitlines()

    grid = {(x,y): val
            for y, row in enumerate(grid_lines, start=1)
            for x, val in enumerate(row, start=1)
            if val != ' '}

    width = max(map(len, grid_lines))
    height = len(grid_lines)

    wrapper = wrap_fn_factory(grid, width, height)

    x, y = s.index('.')+1, 1
    dx, dy = 1, 0

    for step, turn in parse_path(path):
        for _ in range(step):
            val = grid.get((x+dx, y+dy))
            if val == '.':
                x, y = x+dx, y+dy
                continue

            if val is None:
                # Fell off the edge, wrap around
                n, nd = wrapper(x, y, dx, dy)

                if grid[n] == '.':
                    (x, y), (dx, dy) = n, nd
                    continue

            # Hit a wall
            break

        if turn == 'R':
            dy, dx = dx, -dy
        elif turn == 'L':
            dx, dy = dy, -dx
        else:
            assert(turn == '')

    facing_val = {
        (1, 0): 0,
        (0, 1): 1,
        (-1, 0): 2,
        (0, -1): 3,
    }

    return 1000 * y + 4 * x + facing_val[dx,dy]

def simple_wrap_factory(grid, width, height):
    square_dim = math.isqrt(len(grid)//6)

    def wrap_fn(x, y, dx, dy):
        # Change nx to the opposite side of the map (plus 1 to be in bounds)
        nx, ny = x - dx * width + dx, y - dy * height + dy

        while (nx, ny) not in grid:
            nx, ny = nx + dx * square_dim, ny + dy * square_dim

        return (nx, ny), (dx, dy)

    return wrap_fn

def part1(s):
    answer = solve(s, simple_wrap_factory)

    lib.aoc.give_answer(2022, 22, 1, answer)

def fold_cubenet(square_positions, x_axis_2d, y_axis_2d):
    assert(len(square_positions) == 6)

    x_axis = lib.graphics.Vec3D(*x_axis_2d, 0)
    y_axis = lib.graphics.Vec3D(*y_axis_2d, 0)

    assert(x_axis.magnitude == 1)
    assert(y_axis.magnitude == 1)
    assert(x_axis.dot(y_axis) == 0)

    csys = (x_axis, y_axis, x_axis.cross(y_axis))

    face_positions = []
    coord_systems = []

    # Set up 3D cube faces
    for square_pos in square_positions:
        # Offset faces by 2 instead of 1 for easier folding math
        face_positions.append(lib.graphics.Point3D(*square_pos, 0) * 2)
        coord_systems.append(csys)

    square_pos_to_face_num = {pos: f for f, pos in enumerate(square_positions)}

    adjacencies = collections.defaultdict(list)
    fold_edges = set()

    # Find face adjacencies/edges
    for f, (fx, fy) in enumerate(square_positions):
        for dx, dy in (x_axis_2d, y_axis_2d):
            square = fx+dx, fy+dy
            f2 = square_pos_to_face_num.get(square)
            if f2 is not None:
                adjacencies[f].append(f2)
                adjacencies[f2].append(f)
                fold_edges.add((f, f2))

    # Valid cube nets have 5 fold edges
    assert(len(fold_edges) == 5)

    # The fold axis is rotated to z for each edge, just fold around that
    UNIT_FOLD = lib.graphics.Mat3D(lib.graphics.Y_AXIS,
                                   -lib.graphics.X_AXIS,
                                   lib.graphics.Z_AXIS)

    def get_fold_faces(f, source_to_skip):
        for f2 in adjacencies[f]:
            if f2 == source_to_skip:
                continue
            yield from get_fold_faces(f2, f)
        yield f

    # Fold along edges
    for j, (f0, f1) in enumerate(fold_edges):
        to_fold = list(get_fold_faces(f1, f0))

        if len(to_fold) > 3:
            # We can fold fewer faces if we swap f0 and f1
            f0, f1 = f1, f0
            to_fold = list(get_fold_faces(f1, f0))

        p0, p1 = face_positions[f0], face_positions[f1]

        # Shift the faces so the fold line is at the origin
        midpoint = (p0 + p1) // 2
        for i in range(len(face_positions)):
            face_positions[i] -= midpoint

        local_right, local_up, local_in = coord_systems[f0]
        direct = (p1 - p0) // 2 # Faces are 2 units away

        # Local c want to fold from the face direction into the cube
        to_csys = lib.graphics.Mat3D(direct, local_in)

        # Transform from the csys to global, fold along Z, then transform back
        m = to_csys.transposed() * UNIT_FOLD * to_csys

        for f in to_fold:
            face_positions[f] = m * face_positions[f]

            local_right, local_up, local_in = coord_systems[f]
            coord_systems[f] = m * local_right, m * local_up, m * local_in

    # Verify that no faces ended up overlapping
    assert(len(set(face_positions)) == 6)

    return face_positions, coord_systems

def cubenet_wrap_factory(grid, width, height):
    square_dim = math.isqrt(len(grid)//6)

    square_positions = [] # 2D map

    # Set up 2D square cubenet
    for y in range(1, height+1, square_dim):
        for x in range(1, width+1, square_dim):
            if grid.get((x, y)) is not None:
                square_pos = ((x - 1) // square_dim, (y - 1) // square_dim)
                square_positions.append(square_pos)

    face_positions, coord_systems = fold_cubenet(square_positions,
                                                 (1, 0),
                                                 (0, -1))

    square_pos_to_face_num = {pos: f for f, pos in enumerate(square_positions)}

    # Final position lookup
    face_pos_to_face_num = {pos: f for f, pos in enumerate(face_positions)}

    def wrap_fn(x, y, dx, dy):
        # Find the neighboring cube face
        square_pos = ((x - 1) // square_dim, (y - 1) // square_dim)

        face = square_pos_to_face_num[square_pos]
        pos = face_positions[face]
        local_right, local_up, local_in = coord_systems[face]

        # Find the neighboring face
        # Move 1 unit in the local csys based on the movement vector
        # Then move 1 unit "in" to find the next face position
        # Note: Negate dy as -y in 2D is +y in 3D
        next_pos = pos + local_right * dx + local_up * -dy + local_in
        next_face = face_pos_to_face_num[next_pos]

        # Compute next movement vector. Note that in 3D we're moving by local_in
        # Note: Negate dy as -y in 2D is +y in 3D
        next_right, next_up, next_in = coord_systems[next_face]
        next_dx = int(local_in.dot(next_right))
        next_dy = -int(local_in.dot(next_up))

        # Local offsets into the source square
        off_x, off_y = (x - 1) % square_dim, (y - 1) % square_dim

        # Compute local offsets into destination square
        # Cases ordered by most common to least common
        if dx == next_dy and dy == next_dx:
            # X lines up with opposite Y or Y with opposite X
            # Ascending vs descending swaps (low with high or high with low)
            next_off_x = square_dim - 1 - off_y
            next_off_y = square_dim - 1 - off_x
        elif -dx == next_dx and -dy == next_dy:
            # X lines up with X or Y with Y
            # Ascending vs descending swaps (low with low or high with high)
            next_off_x = off_x if dx != 0 else square_dim - 1 - off_x
            next_off_y = off_y if dy != 0 else square_dim - 1 - off_y
        elif -dx == next_dy and -dy == next_dx:
            # X lines up with Y
            # Both in ascending order (low with low or high with high)
            next_off_x = off_y
            next_off_y = off_x
        elif dx == next_dx and dy == next_dy:
            # X lines up with opposite X or Y with opposite Y
            # Both in ascending order (low with high)
            next_off_x = off_x if dx == 0 else square_dim - 1 - off_x
            next_off_y = off_y if dy == 0 else square_dim - 1 - off_y
        else:
            assert(False)

        # Finally, compute the final destination 2D coordinate
        next_square_x, next_square_y = square_positions[next_face]

        next_x = next_square_x * square_dim + next_off_x + 1
        next_y = next_square_y * square_dim + next_off_y + 1

        return (next_x, next_y), (next_dx, next_dy)

    return wrap_fn

def part2(s):
    answer = solve(s, cubenet_wrap_factory)

    lib.aoc.give_answer(2022, 22, 2, answer)

INPUT = lib.aoc.get_input(2022, 22)
part1(INPUT)
part2(INPUT)
