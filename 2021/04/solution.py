import lib.aoc
import lib.grid

class Board:
    def __init__(self, lines):
        board = lib.grid.FixedGrid.parse(lines,
                                         linesplit_fn=lambda line: line.split(),
                                         value_fn=int)

        assert(board.width == 5 and board.height == 5)

        self._nums = {val: c
                      for c, val in board.items()}
        self._seen = set()

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

    lib.aoc.give_answer(2021, 4, 1, answer)

def part2(s):
    nums, boards = parse(s)

    while True:
        answer, nums = find_winning_score(boards, nums)
        boards = [b for b in boards if not b.winning]
        if 0 == len(boards):
            break

    lib.aoc.give_answer(2021, 4, 2, answer)

INPUT = lib.aoc.get_input(2021, 4)
part1(INPUT)
part2(INPUT)
