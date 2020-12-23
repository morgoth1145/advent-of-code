import helpers.input

class LinkedCup:
    __slots__ = ('next', 'num')
    def __init__(self, num):
        self.next = None
        self.num = num

def play_cups(cup_order, turns):
    max_cup = max(cup_order)
    assert(min(cup_order) == 1)
    assert(len(cup_order) == max_cup)
    lookup = [None] * (max_cup + 1)
    for n in cup_order:
        lookup[n] = LinkedCup(n)
    for n, nnext in zip(cup_order, cup_order[1:]):
        lookup[n].next = lookup[nnext]
    lookup[cup_order[-1]].next = lookup[cup_order[0]]
    current = lookup[cup_order[0]]
    for i in range(turns):
        picked = []
        next_picked = current.next
        for _ in range(3):
            picked.append(next_picked)
            next_picked = next_picked.next
        current.next = next_picked
        dest = current.num-1
        if dest < 1:
            dest = max_cup
        while dest in [p.num for p in picked]:
            dest -= 1
            if dest < 1:
                dest = max_cup
        dest_obj = lookup[dest]
        picked[-1].next = dest_obj.next
        dest_obj.next = picked[0]
        current = current.next
    return lookup[1]

def part1(s):
    cups = list(map(int, s))
    current = play_cups(cups, 100)
    order = []
    while True:
        current = current.next
        if current.num == 1:
            break
        order.append(current.num)
    answer = ''.join(map(str, order))
    print(f'The answer to part one is {answer}')

def part2(s):
    seed = list(map(int, s))
    cups = seed + list(range(max(seed)+1, 1000001))
    one = play_cups(cups, 10000000)
    a = one.next
    b = a.next
    answer = a.num*b.num
    print(f'The answer to part one is {answer}')

INPUT = helpers.input.get_input(2020, 23)

part1(INPUT)
part2(INPUT)
