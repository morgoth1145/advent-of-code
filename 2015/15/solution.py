import lib.aoc

def get_possible_sums(target, nums):
    if nums == 1:
        return [(target,)]

    options = []
    for n in range(target+1):
        for opt in get_possible_sums(target-n, nums-1):
            options.append((n,) + opt)
    return options

def optimize(s, teaspoons, calorie_requirement=None):
    properties = []
    all_calories = []

    for line in s.splitlines():
        _, _, cap, _, dur, _, flav, _, texture, _, cal = line.split()

        properties.append((int(cap[:-1]),
                           int(dur[:-1]),
                           int(flav[:-1]),
                           int(texture[:-1])))
        all_calories.append(int(cal))

    best = 0

    for weights in get_possible_sums(teaspoons, len(properties)):
        prop_sums = [0] * len(properties)
        calories = 0

        for weight, props, cals in zip(weights, properties, all_calories):
            calories += weight * cals
            for i in range(len(prop_sums)):
                prop_sums[i] += weight * props[i]

        if calorie_requirement is not None and calories != calorie_requirement:
            continue

        score = 1
        for prop in prop_sums:
            score *= max(prop, 0)

        best = max(score, best)

    return best

def part1(s):
    answer = optimize(s, 100)

    lib.aoc.give_answer(2015, 15, 1, answer)

def part2(s):
    answer = optimize(s, 100, 500)

    lib.aoc.give_answer(2015, 15, 2, answer)

INPUT = lib.aoc.get_input(2015, 15)
part1(INPUT)
part2(INPUT)
