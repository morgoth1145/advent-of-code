import helpers.input

def part1(s):
    answer = 0
    FIELDS = {'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid', 'cid'}
    for passport in s.split('\n\n'):
        seen = set()
        for part in passport.split():
            f, _ = part.split(':')
            seen.add(f)
        if 'cid' not in seen:
            seen.add('cid')
        if seen == FIELDS:
            answer += 1
    print(f'The answer to part one is {answer}')

def part2(s):
    pass

INPUT = helpers.input.get_input(2020, 4)
part1(INPUT)
part2(INPUT)
