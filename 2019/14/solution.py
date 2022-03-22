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

def create(recipes, count, name, surplus=collections.Counter()):
    if name == 'ORE':
        return collections.Counter(), surplus

    spent = collections.Counter()

    amount_created, ingredients = recipes[name]

    used_from_surplus = min(count, surplus[name])
    surplus[name] -= used_from_surplus
    spent[name] += used_from_surplus
    count -= used_from_surplus

    if count == 0:
        return spent, surplus

    times_to_make = (count + amount_created - 1) // amount_created

    # Record any surplus that we created
    surplus[name] += amount_created * times_to_make - count

    for ingredient_count, ingredient_name in ingredients:
        sub_spent, surplus = create(recipes,
                                    times_to_make * ingredient_count,
                                    ingredient_name)
        spent += sub_spent
        spent[ingredient_name] += times_to_make * ingredient_count

    return spent, surplus

def part1(s):
    recipes = parse_recipes(s)

    spent, surplus = create(recipes, 1, 'FUEL')

    answer = spent['ORE'] + surplus['ORE']

    print(f'The answer to part one is {answer}')

def part2(s):
    pass

INPUT = lib.aoc.get_input(2019, 14)
part1(INPUT)
part2(INPUT)
