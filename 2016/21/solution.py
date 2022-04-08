import lib.aoc

def make_swap_letter_fn(x, y):
    t = str.maketrans(x+y, y+x)
    def impl(password):
        return password.translate(t)
    return impl

def make_swap_pos_fn(x, y):
    def impl(password):
        password = list(password)
        password[x], password[y] = password[y], password[x]
        return ''.join(password)
    return impl

def rotate_left(password, x):
    x %= len(password)
    return password[x:] + password[:x]

def make_rotate_based_fn(x):
    def impl(password):
        idx = password.index(x)
        right_rotate = 1 + idx + (idx >= 4)
        return rotate_left(password, -right_rotate)
    return impl

def make_rotate_based_inverse_fn(x):
    known_inverses = {}
    def impl(password):
        inverses = known_inverses.get(len(password))
        if inverses is None:
            inverses = [[] for _ in range(len(password))]
            for idx in range(len(password)):
                right_rotate = 1 + idx + (idx >= 4)
                target_idx = (idx + right_rotate) % len(password)
                inverses[target_idx].append(right_rotate)
            inverses = [i[0] if len(i) == 1 else None
                        for i in inverses]
            known_inverses[len(password)] = inverses
        left_rot = inverses[password.index(x)]
        assert(left_rot is not None)
        return rotate_left(password, left_rot)
    return impl

def make_rotate_fn(direction, x):
    if direction == 'right':
        x = -x
    def impl(password):
        return rotate_left(password, x)
    return impl

def make_reverse_fn(x, y):
    def impl(password):
        return password[:x] + password[x:y+1][::-1] + password[y+1:]
    return impl

def make_move_fn(x, y):
    def impl(password):
        password = list(password)
        c = password.pop(x)
        password.insert(y, c)
        return ''.join(password)
    return impl

def parse_instructions(s):
    for line in s.splitlines():
        inst = line.split()
        if inst[0] == 'swap':
            if inst[1] == 'letter':
                apply = make_swap_letter_fn(inst[2], inst[5])
                yield apply, apply # Self-inverse
            else:
                assert(inst[1] == 'position')
                apply = make_swap_pos_fn(int(inst[2]), int(inst[5]))
                yield apply, apply # Self-inverse
        elif inst[0] == 'rotate':
            if inst[1] == 'based':
                yield (make_rotate_based_fn(inst[6]),
                       make_rotate_based_inverse_fn(inst[6]))
            else:
                # The inverse is just rotating the other way
                yield (make_rotate_fn(inst[1], int(inst[2])),
                       make_rotate_fn(inst[1], -int(inst[2])))
        elif inst[0] == 'reverse':
            apply = make_reverse_fn(int(inst[2]), int(inst[4]))
            yield apply, apply # Self-inverse
        elif inst[0] == 'move':
            # The inverse is just moving y to x
            yield (make_move_fn(int(inst[2]), int(inst[5])),
                   make_move_fn(int(inst[5]), int(inst[2])))
        else:
            assert(False)

def part1(s):
    answer = 'abcdefgh'

    for apply, inverse in parse_instructions(s):
        answer = apply(answer)

    lib.aoc.give_answer(2016, 21, 1, answer)

def part2(s):
    answer = 'fbgdceah'

    for apply, inverse in list(parse_instructions(s))[::-1]:
        answer = inverse(answer)

    lib.aoc.give_answer(2016, 21, 2, answer)

INPUT = lib.aoc.get_input(2016, 21)
part1(INPUT)
part2(INPUT)
