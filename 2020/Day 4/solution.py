import helpers.input

def parse_passport(passport):
    out = {}
    for part in passport.split():
        f, val = part.split(':')
        out[f] = val
    return out

def part1(s):
    answer = 0
    FIELDS = {'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid', 'cid'}
    for passport in s.split('\n\n'):
        passport = parse_passport(passport)
        seen = set(passport.keys())
        if 'cid' not in seen:
            seen.add('cid')
        if seen == FIELDS:
            answer += 1
    print(f'The answer to part one is {answer}')

def part2(s):
    answer = 0
    for passport in s.split('\n\n'):
        passport = parse_passport(passport)
        if not (1920 <= int(passport.get('byr', 0)) <= 2002):
            continue
        if not (2010 <= int(passport.get('iyr', 0)) <= 2020):
            continue
        if not (2020 <= int(passport.get('eyr', 0)) <= 2030):
            continue
        if 'hgt' not in passport:
            continue
        hgt = passport['hgt']
        if hgt[-2:] == 'cm':
            if not (150 <= int(hgt[:-2]) <= 193):
                continue
        elif hgt[-2:] == 'in':
            if not (59 <= int(hgt[:-2]) <= 76):
                continue
        else:
            continue
        if 'hcl' not in passport:
            continue
        hcl = passport.get('hcl')
        if hcl[0] != '#':
            continue
        if any(c not in '0123456789abcdef' for c in hcl[1:]):
            continue
        if passport.get('ecl') not in ('amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'):
            continue
        if 'pid' not in passport:
            continue
        pid = passport['pid']
        if len(pid) != 9 or any(c not in '0123456789' for c in pid):
            continue
        answer += 1
    print(f'The answer to part two is {answer}')

INPUT = helpers.input.get_input(2020, 4)
part1(INPUT)
part2(INPUT)
