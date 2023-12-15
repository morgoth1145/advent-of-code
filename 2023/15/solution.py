import lib.aoc

def HASH(s):
    v = 0
    for c in s:
        v = ((v + ord(c)) * 17) % 256
    return v

def part1(s):
    answer = sum(map(HASH, s.split(',')))

    lib.aoc.give_answer(2023, 15, 1, answer)

def part2(s):
    hashmap = [[] for _ in range(256)]

    for step in s.replace('=','-').split(','):
        label, focal = step.split('-')
        box = hashmap[HASH(label)]
        if focal == '':
            # Was a dash, remove from the box
            box[:] = [entry for entry in box
                      if entry[0] != label]
        else:
            # Was an equals sign, add to the box
            focal = int(focal)
            if label in [entry[0] for entry in box]:
                box[:] = [(label, focal) if entry[0] == label else entry
                          for entry in box]
            else:
                box.append((label, focal))

    answer = sum(box_idx * idx * focal
                 for box_idx, box in enumerate(hashmap, start=1)
                 for idx, (_, focal) in enumerate(box, start=1))

    lib.aoc.give_answer(2023, 15, 2, answer)

INPUT = lib.aoc.get_input(2023, 15)
part1(INPUT)
part2(INPUT)
