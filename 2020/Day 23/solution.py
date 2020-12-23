import helpers.input

def move(cups):
    picked = cups[1:4]
    cups[1:4] = []
    dest = cups[0]-1
    if dest < min(cups):
        dest = max(cups)
    while dest in picked:
        dest -= 1
        if dest < min(cups):
            dest = max(cups)
    idx = cups.index(dest)
    cups[:idx+1] = cups[:idx+1] + picked
    cups = cups[1:] + cups[:1]
    return cups

def part1(s):
    cups = list(map(int, s))
    for _ in range(100):
        cups = move(cups[:])
    idx = cups.index(1)
    order = cups[idx+1:] + cups[:idx]
    answer = ''.join(map(str, order))
    print(f'The answer to part one is {answer}')

class LinkedCup:
    def __init__(self, num):
        self.next = None
        self.num = num

def linked_move(current, lookup, max_cup):
    picked = []
    in_hand = set()
    next_picked = current.next
    for _ in range(3):
        in_hand.add(next_picked.num)
        picked.append(next_picked)
        next_picked = next_picked.next
    current.next = next_picked
    dest = current.num-1
    if dest < 1:
        dest = max_cup
    while dest in in_hand:
        dest -= 1
        if dest < 1:
            dest = max_cup
    dest_obj = lookup[dest]
    picked[-1].next = dest_obj.next
    dest_obj.next = picked[0]

def part2(s):
    MAXIMUM = 1000000
    TURNS = 10000000

    seed = list(map(int, s))
    lookup = [None] * (MAXIMUM + 1)
    for n in range(1, MAXIMUM+1):
        lookup[n] = LinkedCup(n)
    for n in range(1, MAXIMUM):
        lookup[n].next = lookup[n+1]
    for n, nnext in zip(seed, seed[1:] + [max(seed)+1]):
        lookup[n].next = lookup[nnext]
    lookup[MAXIMUM].next = lookup[seed[0]]
    current = lookup[seed[0]]
    for i in range(TURNS):
        linked_move(current, lookup, MAXIMUM)
        current = current.next
    one = lookup[1]
    a = one.next
    b = a.next
    answer = a.num*b.num
    print(f'The answer to part one is {answer}')

INPUT = helpers.input.get_input(2020, 23)

part1(INPUT)
part2(INPUT)
