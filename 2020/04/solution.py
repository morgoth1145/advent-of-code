import lib.aoc

def parse_passports(s):
    for record in s.split('\n\n'):
        passport = {}
        for part in record.split():
            f, val = part.split(':')
            passport[f] = val
        yield passport

def part1(s):
    answer = 0
    FIELDS = {'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid', 'cid'}
    for passport in parse_passports(s):
        seen = set(passport.keys())
        if 'cid' not in seen:
            seen.add('cid')
        if seen == FIELDS:
            answer += 1
    lib.aoc.give_answer(2020, 4, 1, answer)

def validate_hgt(hgt):
    if hgt is None:
        return False
    if hgt[-2:] == 'cm':
        return 150 <= int(hgt[:-2]) <= 193
    if hgt[-2:] == 'in':
        return 59 <= int(hgt[:-2]) <= 76
    return False

def validate_hcl(hcl):
    return (hcl is not None and
            hcl[0] == '#' and
            all(c in '0123456789abcdef' for c in hcl[1:]))

def validate_pid(pid):
    return (pid is not None and
            len(pid) == 9 and
            all(c in '0123456789' for c in pid))

def part2(s):
    answer = 0
    for passport in parse_passports(s):
        if (1920 <= int(passport.get('byr', 0)) <= 2002 and
            2010 <= int(passport.get('iyr', 0)) <= 2020 and
            2020 <= int(passport.get('eyr', 0)) <= 2030 and
            validate_hgt(passport.get('hgt')) and
            validate_hcl(passport.get('hcl')) and
            passport.get('ecl') in ('amb',
                                    'blu',
                                    'brn',
                                    'gry',
                                    'grn',
                                    'hzl',
                                    'oth') and
            validate_pid(passport.get('pid'))):
            answer += 1
    lib.aoc.give_answer(2020, 4, 2, answer)

INPUT = lib.aoc.get_input(2020, 4)
part1(INPUT)
part2(INPUT)
