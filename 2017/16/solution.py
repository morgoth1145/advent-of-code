import lib.aoc

def dance(order, s):
    for inst in s.split(','):
        if inst[0] == 's':
            x = int(inst[1:])
            order = order[-x:] + order[:-x]
        elif inst[0] == 'x':
            a, b = sorted(map(int, inst[1:].split('/')))
            order = order[:a] + order[b] + order[a+1:b] + order[a] + order[b+1:]
        elif inst[0] == 'p':
            a = inst[1]
            assert(inst[2] == '/')
            b = inst[3]
            order = order.translate(str.maketrans(a+b, b+a))
        else:
            assert(False)

    return order

def part1(s):
    answer = dance('abcdefghijklmnop', s)

    lib.aoc.give_answer(2017, 16, 1, answer)

def part2(s):
    answer = 'abcdefghijklmnop'

    order_to_iter = {
        answer: 0
    }

    while True:
        answer = dance(answer, s)
        if answer in order_to_iter:
            break

        order_to_iter[answer] = len(order_to_iter)

    iteration = len(order_to_iter)
    cycle = iteration - order_to_iter[answer]
    remaining = (1000000000 - iteration) % cycle

    for _ in range(remaining):
        answer = dance(answer, s)

    lib.aoc.give_answer(2017, 16, 2, answer)

INPUT = lib.aoc.get_input(2017, 16)
part1(INPUT)
part2(INPUT)
