import re

import helpers.input

def parse_foods(s):
    foods = []
    for line in s.splitlines():
        m = re.fullmatch('([a-zA-Z ]+) \(contains ([a-zA-Z ,]+)\)', line)
        ingredients = set(m.group(1).split())
        allergens = set(m.group(2).split(', '))
        foods.append((ingredients, allergens))
    return foods

def part1(s):
    foods = parse_foods(s)

    all_ingredients = set()
    all_allergens = set()

    for ingredients, allergens in foods:
        all_ingredients |= ingredients
        all_allergens |= allergens

    possible_allergens = set()

    for allergen in all_allergens:
        possibilities = set(all_ingredients)
        for ingredients, allergens in foods:
            if allergen in allergens:
                possibilities &= ingredients
        possible_allergens |= possibilities

    safe_ingredients = all_ingredients - possible_allergens

    answer = 0
    for ingredients, allergens in foods:
        answer += len(ingredients & safe_ingredients)
    print(f'The answer to part one is {answer}')

def part2(s):
    foods = parse_foods(s)

    all_ingredients = set()
    all_allergens = set()

    for ingredients, allergens in foods:
        all_ingredients |= ingredients
        all_allergens |= allergens

    possible_bad_ingredients = set()

    for allergen in all_allergens:
        possibilities = set(all_ingredients)
        for ingredients, allergens in foods:
            if allergen in allergens:
                possibilities &= ingredients
        possible_bad_ingredients |= possibilities

    assert(len(possible_bad_ingredients) == len(all_allergens))

    allergen_to_triggers = {}
    for allergen in all_allergens:
        allergen_to_triggers[allergen] = set(possible_bad_ingredients)

    for ingredients, allergens in foods:
        for allergen in allergens:
            allergen_to_triggers[allergen] &= ingredients

    def solved():
        for thing in allergen_to_triggers.values():
            if len(thing) > 1:
                return False
        return True

    while not solved():
        identified = set()
        for thing in allergen_to_triggers.values():
            if len(thing) == 1:
                identified |= thing
        for allergen, thing in allergen_to_triggers.items():
            if len(thing) > 1:
                allergen_to_triggers[allergen] -= identified

    stuff = sorted(allergen_to_triggers.items())
    answer = ','.join(list(trigger)[0] for _,trigger in stuff)

    print(f'The answer to part two is {answer}')

INPUT = helpers.input.get_input(2020, 21)

part1(INPUT)
part2(INPUT)
