import lib.aoc

letters = 'abcdefghijklmnopqrstuvwxyz'

def password_to_n(s):
    n = 0
    for c in s:
        n *= 26
        n += letters.index(c)
    return n

def n_to_password(n):
    out = []
    while n:
        c = letters[n % 26]
        n //= 26
        out.append(c)
    return ''.join(out[::-1])

def next_password(s):
    char_nums = [letters.index(c) for c in n_to_password(password_to_n(s)+1)]
    for c in 'iol':
        for idx in range(len(char_nums)):
            if char_nums[idx] == letters.index(c):
                char_nums[idx] += 1
                for j in range(idx+1, len(char_nums)):
                    char_nums[j] = 0
                break
    
    return ''.join(letters[i] for i in char_nums)

def check_password(s):
    if any(c in s
           for c in 'iol'):
        return False

    char_nums = [letters.index(c) for c in s]

    if all(char_nums[i]+1 != char_nums[i+1] or char_nums[i]+2 != char_nums[i+2]
           for i in range(len(char_nums)-2)):
        return False

    for i in range(len(s)-1):
        if s[i] == s[i+1]:
            for j in range(i+2, len(s)-1):
                if s[j] == s[j+1]:
                    return True

    return False

def part1(s):
    while not check_password(s):
        s = next_password(s)

    answer = s

    print(f'The answer to part one is {answer}')

def part2(s):
    while not check_password(s):
        s = next_password(s)
    s = next_password(s)
    while not check_password(s):
        s = next_password(s)

    answer = s

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2015, 11)
part1(INPUT)
part2(INPUT)
