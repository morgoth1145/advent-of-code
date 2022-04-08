import lib.aoc

def count_matching(s, *rules):
    answer = 0
    for line in s.splitlines():
        if all(r(line) for r in rules):
            answer += 1
    return answer

def rule1(s):
    return sum(1
               for c in s
               if c in 'aeiou') >= 3

def rule2(s):
    return any(s[i-1] == s[i]
               for i in range(1, len(s)))

def rule3(s):
    return not any(bad in s
                   for bad in ('ab', 'cd', 'pq', 'xy'))

def part1(s):
    answer = count_matching(s, rule1, rule2, rule3)

    lib.aoc.give_answer(2015, 5, 1, answer)

def rule4(s):
    return any(s[idx-1:idx+1] in s[idx+1:]
               for idx in range(1, len(s)))

def rule5(s):
    return any(s[i-2] == s[i]
               for i in range(2, len(s)))

def part2(s):
    answer = count_matching(s, rule4, rule5)

    lib.aoc.give_answer(2015, 5, 2, answer)

INPUT = lib.aoc.get_input(2015, 5)
part1(INPUT)
part2(INPUT)
