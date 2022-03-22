import collections

import lib.aoc

def parse_recipes(s):
    recipes = {}

    for line in s.splitlines():
        lhs, rhs = line.split(' => ')

        ingredients = []
        for part in lhs.split(', '):
            count, name = part.split()
            ingredients.append((int(count), name))

        count, name = rhs.split()

        recipes[name] = (int(count), ingredients)

    return recipes

def ore_required_for_fuel(recipes, fuel_count):
    spent = collections.Counter()
    surplus = collections.Counter()

    def create(recipes, count, name):
        if name == 'ORE':
            return

        amount_created, ingredients = recipes[name]

        used_from_surplus = min(count, surplus[name])
        surplus[name] -= used_from_surplus
        spent[name] += used_from_surplus
        count -= used_from_surplus

        if count == 0:
            return

        times_to_make = (count + amount_created - 1) // amount_created

        # Record any surplus that we created
        surplus[name] += amount_created * times_to_make - count

        for ingredient_count, ingredient_name in ingredients:
            create(recipes, times_to_make * ingredient_count, ingredient_name)

            spent[ingredient_name] += times_to_make * ingredient_count

    create(recipes, fuel_count, 'FUEL')

    assert(surplus['ORE'] == 0)

    return spent['ORE']

def part1(s):
    recipes = parse_recipes(s)

    answer = ore_required_for_fuel(recipes, 1)

    print(f'The answer to part one is {answer}')

def part2(s):
    recipes = parse_recipes(s)

    MAXIMUM_ORE = 1000000000000

    # Find a range where the upper bound is more fuel than we can create
    low_fuel = 1
    high_fuel = 2
    while ore_required_for_fuel(recipes, high_fuel) <= MAXIMUM_ORE:
        low_fuel = high_fuel
        high_fuel *= 2

    # Binary search to find the maximum fuel we can create
    while low_fuel+1 < high_fuel:
        mid_fuel = (low_fuel + high_fuel) // 2

        required = ore_required_for_fuel(recipes, mid_fuel)
        if required <= MAXIMUM_ORE:
            low_fuel = mid_fuel
        else:
            high_fuel = mid_fuel

    answer = low_fuel

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2019, 14)
part1(INPUT)
part2(INPUT)
