import lib.aoc

def parse_instructions(s):
    for line in s.splitlines():
        yield line.split()

def scramble(password, instructions):
    for inst in instructions:
        op = inst[0]
        if op == 'swap':
            if inst[1] == 'letter':
                a = inst[2]
                b = inst[5]
                password = password.translate(str.maketrans(a+b, b+a))
            else:
                assert(inst[1] == 'position')
                a = int(inst[2])
                b = int(inst[5])
                password = list(password)
                password[a], password[b] = password[b], password[a]
                password = ''.join(password)
        elif op == 'rotate':
            if inst[1] == 'based':
                c = inst[6]
                idx = password.index(c)
                rotate_n = 1 + idx
                if idx >= 4:
                    rotate_n += 1
                rotate_n %= len(password)
                password = password[-rotate_n:] + password[:-rotate_n]
            else:
                x = int(inst[2])
                if inst[1] == 'left':
                    password = password[x:] + password[:x]
                else:
                    assert(inst[1] == 'right')
                    password = password[-x:] + password[:-x]
        elif op == 'reverse':
            x = int(inst[2])
            y = int(inst[4])
            password = password[:x] + password[x:y+1][::-1] + password[y+1:]
        elif op == 'move':
            x = int(inst[2])
            y = int(inst[5])
            password = list(password)
            c = password.pop(x)
            password.insert(y, c)
            password = ''.join(password)
        else:
            assert(False)

    return password

def part1(s):
    answer = scramble('abcdefgh', parse_instructions(s))

    print(f'The answer to part one is {answer}')

def undo(password, inst):
    op = inst[0]
    if op == 'swap':
        if inst[1] == 'letter':
            a = inst[2]
            b = inst[5]
            yield password.translate(str.maketrans(a+b, b+a))
        else:
            assert(inst[1] == 'position')
            a = int(inst[2])
            b = int(inst[5])
            password = list(password)
            password[a], password[b] = password[b], password[a]
            yield ''.join(password)
    elif op == 'rotate':
        if inst[1] == 'based':
            c = inst[6]
            for idx in range(len(password)):
                rotate_n = 1 + idx
                if idx >= 4:
                    rotate_n += 1
                rotate_n %= len(password)

                cand = password[rotate_n:] + password[:rotate_n]
                if cand[idx] == c:
                    yield cand
        else:
            x = int(inst[2])
            if inst[1] == 'left':
                # Rotate right as the inverse
                yield password[-x:] + password[:-x]
            else:
                assert(inst[1] == 'right')
                # Rotate left as the inverse
                yield password[x:] + password[:x]
    elif op == 'reverse':
        x = int(inst[2])
        y = int(inst[4])
        yield password[:x] + password[x:y+1][::-1] + password[y+1:]
    elif op == 'move':
        x = int(inst[2])
        y = int(inst[5])
        password = list(password)
        # Inverted
        c = password.pop(y)
        password.insert(x, c)
        yield ''.join(password)
    else:
        assert(False)

def unscramble(password, instructions):
    candidates = {password}

    instructions = list(instructions)[::-1]
    for inst in instructions:
        new_cands = set()

        for p in candidates:
            for c in undo(p, inst):
                new_cands.add(c)

        candidates = new_cands

    candidates = list(candidates)
    if len(candidates) > 1:
        print(candidates)
        assert(False)

    return candidates[0]

def part2(s):
    answer = unscramble('fbgdceah', parse_instructions(s))

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2016, 21)
part1(INPUT)
part2(INPUT)
