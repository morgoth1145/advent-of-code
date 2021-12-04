import lib.aoc

class Board:
    def __init__(self, lines):
        rows = [list(map(int, l.strip().split()))
                for l in lines.split('\n')]
        self._nums = {}
        self._seen = set()

        assert(len(rows[0]) == 5)
        assert(len(rows) == 5)

        for x in range(5):
            for y in range(5):
                self._nums[rows[x][y]] = (x, y)

    def mark(self, n):
        coord = self._nums.get(n)
        if coord is not None:
            self._seen.add(coord)

    @property
    def winning(self):
        for x in range(5):
            if all((x, y) in self._seen
                   for y in range(5)):
                return True
        for y in range(5):
            if all((x, y) in self._seen
                   for x in range(5)):
                return True
        return False

    def score(self, last_n):
        t = 0
        for val, coord in self._nums.items():
            if coord in self._seen:
                continue
            t += val
        return t * last_n

def parse(s):
    groups = s.split('\n\n')
    nums = list(map(int, groups[0].split(',')))
    groups = groups[1:]

    boards = list(map(Board, groups))

    return nums, boards

def find_winning_score(boards, nums):
    for idx, n in enumerate(nums):
        for b in boards:
            b.mark(n)
        for b in boards:
            if b.winning:
                return b.score(n), nums[idx+1:]

def part1(s):
    nums, boards = parse(s)

    answer, _ = find_winning_score(boards, nums)

    print(f'The answer to part one is {answer}')

def part2(s):
    nums, boards = parse(s)

    while True:
        answer, nums = find_winning_score(boards, nums)
        boards = [b for b in boards if not b.winning]
        if 0 == len(boards):
            break

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2021, 4)
part1(INPUT)
part2(INPUT)
