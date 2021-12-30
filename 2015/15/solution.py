import lib.aoc

def parse_input(s):
    for line in s.splitlines():
        name, _, cap, _, dur, _, flav, _, texture, _, cal = line.split()
        name = name[:-1]
        cap = int(cap[:-1])
        dur = int(dur[:-1])
        flav = int(flav[:-1])
        texture = int(texture[:-1])
        cal = int(cal)
        yield name, cap, dur, flav, texture, cal

def get_possible_sums(target, nums):
    if nums == 1:
        return [(target,)]

    options = []
    for n in range(target+1):
        for opt in get_possible_sums(target-n, nums-1):
            options.append((n,) + opt)
    return options

def optimize(s, teaspoons, calorie_requirement=None):
    capacities = []
    durabilities = []
    flavors = []
    textures = []
    calories = []

    for name, cap, dur, flav, texture, cal in parse_input(s):
        capacities.append([i * cap for i in range(teaspoons+1)])
        durabilities.append([i * dur for i in range(teaspoons+1)])
        flavors.append([i * flav for i in range(teaspoons+1)])
        textures.append([i * texture for i in range(teaspoons+1)])
        calories.append([i * cal for i in range(teaspoons+1)])

    best = 0

    for weights in get_possible_sums(teaspoons, len(capacities)):
        cap, dur, flavor, texture, cal = 0, 0, 0, 0, 0
        for i, w in enumerate(weights):
            cap += capacities[i][w]
            dur += durabilities[i][w]
            flavor += flavors[i][w]
            texture += textures[i][w]
            cal += calories[i][w]
        if calorie_requirement is not None and cal != calorie_requirement:
            continue
        score = max(cap, 0) * max(dur, 0) * max(flavor, 0) * max(texture, 0)
        best = max(score, best)

    return best

def part1(s):
    answer = optimize(s, 100)

    print(f'The answer to part one is {answer}')

def part2(s):
    answer = optimize(s, 100, 500)

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2015, 15)
part1(INPUT)
part2(INPUT)
