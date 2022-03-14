import lib.aoc

def solve(s, generations):
    groups = s.split('\n\n')

    pots = groups[0].split()[2]
    start = pots.index('#')
    pots = pots.strip('.')

    transitions = {}

    for line in groups[1].splitlines():
        a, b = line.split(' => ')
        transitions[a] = b

    assert(transitions['.....'] == '.')

    memory = {}
    sequence = []

    for gen_num in range(generations):
        sequence.append((start, pots))
        if pots in memory:
            gen_seen, prev_start = memory[pots]
            # Jump ahead!

            repeat_every = gen_num - gen_seen
            shift_per = start - prev_start

            remaining = generations - gen_num
            jump_by = remaining // repeat_every
            start += jump_by * shift_per

            remaining = remaining % repeat_every
            next_start, pots = sequence[gen_seen + remaining]

            start += next_start - prev_start
            break

        memory[pots] = (gen_num, start)

        # The added padding shifts start to the left, though
        # we'll likely shift back at the end
        start -= 2
        pots = '....' + pots + '....'

        pots = ''.join(transitions[pots[i:i+5]]
                       for i in range(len(pots)-4))

        start += pots.index('#')
        pots = pots.strip('.')

    return sum(start + idx
               for idx, c in enumerate(pots)
               if c == '#')

def part1(s):
    answer = solve(s, 20)

    print(f'The answer to part one is {answer}')

def part2(s):
    answer = solve(s, 50000000000)

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2018, 12)
part1(INPUT)
part2(INPUT)
