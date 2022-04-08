import lib.aoc

def parse_action(lines):
    if lines[0] == '    - Write the value 1.':
        write = 1
    else:
        assert(lines[0] == '    - Write the value 0.')
        write = 0

    if lines[1] == '    - Move one slot to the left.':
        move = -1
    else:
        assert(lines[1] == '    - Move one slot to the right.')
        move = 1

    next_state = lines[2].split()[-1][:-1]

    return write, move, next_state

def parse_input(s):
    groups = s.split('\n\n')
    setup = groups[0].splitlines()

    start_state = setup[0].split()[-1][:-1]
    steps = int(setup[1].split()[5])

    states = {}

    for desc in groups[1:]:
        lines = desc.splitlines()

        name = lines[0].split()[-1][:-1]
        assert('  If the current value is 0:' == lines[1])
        zero_action = parse_action(lines[2:5])
        assert('  If the current value is 1:' == lines[5])
        one_action = parse_action(lines[6:9])

        states[name] = (zero_action, one_action)

    return start_state, steps, states

def part1(s):
    start_state, steps, states = parse_input(s)

    tape = {}
    cursor = 0

    s = start_state

    for _ in range(steps):
        val = tape.get(cursor, 0)
        write, move, next_state = states[s][val]
        tape[cursor] = write
        cursor += move
        s = next_state

    answer = sum(tape.values())

    lib.aoc.give_answer(2017, 25, 1, answer)

def part2(s):
    print('There is no part two for Christmas!')

INPUT = lib.aoc.get_input(2017, 25)
part1(INPUT)
part2(INPUT)
