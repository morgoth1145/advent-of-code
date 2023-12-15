import lib.aoc

def the_hash(s):
    v = 0
    for c in s:
        v += ord(c)
        v *= 17
        v %= 256

    return v

def part1(s):
    bits = s.split(',')

    answer = sum(map(the_hash, bits))

    lib.aoc.give_answer(2023, 15, 1, answer)

def part2(s):
    bits = s.split(',')

    hashmap = [[] for _ in range(256)]

    for part in bits:
        if '=' in part:
            label = part[:part.index('=')]
            op = '='
            rest = part[part.index('=')+1:]
            focal = int(rest)

            box_idx = the_hash(label)
            box = hashmap[box_idx]
            replaced = False
            for i in range(len(box)):
                if box[i][0] == label:
                    box[i] = (label, focal)
                    replaced = True
            if not replaced:
                box.append((label, focal))
        elif '-' in part:
            label = part[:part.index('-')]
            op = '-'
            rest = part[part.index('-')+1:]
            assert(len(rest) == 0)

            box_idx = the_hash(label)
            box = hashmap[box_idx]
            for i in range(len(box)):
                if box[i][0] == label:
                    box.pop(i)
                    break
        else:
            assert(False)

    answer = 0

    for box_idx, box in enumerate(hashmap, start=1):
        for idx, (_, focal) in enumerate(box, start=1):
            answer += box_idx * idx * focal

    lib.aoc.give_answer(2023, 15, 2, answer)

INPUT = lib.aoc.get_input(2023, 15)
part1(INPUT)
part2(INPUT)
