import lib.aoc

LETTERS = 'abcdefghijklmnopqrstuvwxyz'
BAD_CHARS = [LETTERS.index(c) for c in 'iol']

def next_legal_password(s):
    nums = list(map(LETTERS.index, s))

    while True:
        for i in range(len(s)-1, -1, -1):
            nums[i] += 1
            if nums[i] == 26:
                nums[i] = 0
            else:
                break

        if any(c in nums for c in BAD_CHARS):
            continue

        if all(nums[i]+1 != nums[i+1] or nums[i]+2 != nums[i+2]
               for i in range(len(nums)-2)):
            continue

        for i in range(len(nums)-3):
            if nums[i] == nums[i+1]:
                for j in range(i+2, len(nums)-1):
                    if nums[j] == nums[j+1]:
                        return ''.join(LETTERS[n] for n in nums)
                break

def part1(s):
    answer = next_legal_password(s)

    print(f'The answer to part one is {answer}')

def part2(s):
    answer = next_legal_password(next_legal_password(s))

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2015, 11)
part1(INPUT)
part2(INPUT)
