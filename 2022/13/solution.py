import json

import lib.aoc

def parse_input(s):
    for group in s.split('\n\n'):
        a, b = group.splitlines()
        a = json.loads(a)
        b = json.loads(b)
        yield a, b

def is_right_order(a, b):
    alen = len(a)
    blen = len(b)
    
    for i in range(min(alen, blen)):
        aitem = a[i]
        bitem = b[i]
        if isinstance(aitem, int) and isinstance(bitem, int):
            if aitem < bitem:
                return True
            if aitem > bitem:
                return False
            continue
        if isinstance(aitem, list) and isinstance(bitem, list):
            subanswer = is_right_order(aitem, bitem)
            if subanswer is not None:
                return subanswer
            continue
        # One of them is an int
        if isinstance(aitem, int):
            aitem = [aitem]
        elif isinstance(bitem, int):
            bitem = [bitem]
        else:
            assert(False)
        subanswer = is_right_order(aitem, bitem)
        if subanswer is not None:
            return subanswer

    if alen < blen:
        return True
    if blen < alen:
        return False

def part1(s):
    data = list(parse_input(s))

    answer = sum(i+1
                 for i, (a, b)
                 in enumerate(data)
                 if is_right_order(a, b) is True)

    lib.aoc.give_answer(2022, 13, 1, answer)

class Wrapper:
    def __init__(self, item):
        self.item = item

    def __lt__(self, other):
        return is_right_order(self.item, other.item)

def part2(s):
    data = list(parse_input(s))

    all_items = []
    for a, b in data:
        all_items += [a, b]

    all_items.append([[2]])
    all_items.append([[6]])

    all_items = sorted(all_items, key=Wrapper)
    assert(is_right_order(all_items[0], all_items[1]))

    a = all_items.index([[2]]) + 1
    b = all_items.index([[6]]) + 1

    answer = a * b

    lib.aoc.give_answer(2022, 13, 2, answer)

INPUT = lib.aoc.get_input(2022, 13)
part1(INPUT)
part2(INPUT)
