from datetime import datetime
import re


CWHT = '\033[97m'
CGRN = '\033[92m'
CEND = '\033[0m'

start = datetime.now()

quest = 'hub_q03'

text_sample1 = open(quest + '_sample_p1.txt').read()
text_p1 = open(quest + '_puzzle_p1.txt').read()

text_sample2 = open(quest + '_sample_p2.txt').read()
text_p2 = open(quest + '_puzzle_p2.txt').read()

text_sample3_1 = open(quest + '_sample_p3_1.txt').read()
text_sample3_2 = open(quest + '_sample_p3_2.txt').read()
text_p3 = open(quest + '_puzzle_p3.txt').read()


def get_all_nums(line):
    return list(map(int, re.findall(r"[+-]?\d+", line.strip())))


class dice:
    def __init__(self, id, faces, seed):
        self.id = id
        self.faces = faces
        self.seed = seed
        self.pulse = seed
        self.roll_number = 1
        self.index = 0

    def roll(self):
        spin = self.roll_number * self.pulse
        self.index = (self.index + spin) % len(self.faces)
        self.pulse += spin
        self.pulse = self.pulse % self.seed
        self.pulse = self.pulse + 1 + self.roll_number + self.seed
        self.roll_number += 1
        res = self.faces[self.index]
        return res


def solve1(text):
    dices = []
    for line in text.splitlines():
        numbers = get_all_nums(line)
        id_ = numbers[0]
        faces = numbers[1:-1]
        seed = numbers[-1]
        d = dice(id_, faces, seed)
        dices.append(d)

    rolls = 0
    score = 0
    target = 10000
    while score < target:
        for d in dices:
            r = d.roll()
            score += r
        rolls += 1
    return rolls


def solve2(text):
    dices = []
    dices_part, num_part = text.split('\n\n')

    for line in dices_part.splitlines():
        numbers = get_all_nums(line)
        id_ = numbers[0]
        faces = numbers[1:-1]
        seed = numbers[-1]
        d = dice(id_, faces, seed)
        dices.append(d)

    nums = [int(x) for x in num_part.splitlines()[0]]

    finised_id = set()
    finished = []
    current_indexes = {d.id: 0 for d in dices}

    while True:
        for d in dices:
            if d.id in finised_id:
                continue
            r = d.roll()
            indx = current_indexes[d.id]
            target_num = nums[indx]

            if r == target_num:
                current_indexes[d.id] += 1
                if current_indexes[d.id] == len(nums):
                    # dice finished
                    finised_id.add(d.id)
                    finished.append(d.id)
        if len(finised_id) == len(dices):
            break

    res = ""
    for n in finished:
        if res != "":
            res += ","
        res += str(n)
    return res


def solve3(text):
    dices = []
    dices_part, nums_part = text.split('\n\n')

    for line in dices_part.splitlines():
        numbers = get_all_nums(line)
        id_ = numbers[0]
        faces = numbers[1:-1]
        seed = numbers[-1]
        d = dice(id_, faces, seed)
        dices.append(d)

    nums = []
    for line in nums_part.splitlines():
        row = []
        for x in line.strip():
            row.append(int(x))
        nums.append(row)

    R = len(nums)
    C = len(nums[0])

    visited_cells = set()
    for d in dices:
        roll1 = d.roll()
        current_paths = set()

        for r in range(R):
            for c in range(C):
                if nums[r][c] == roll1:
                    current_paths.add((r, c))
        while True:
            next_paths = set()
            val = d.roll()
            for r, c in current_paths:
                visited_cells.add((r, c))
                for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1), (0, 0)]:
                    nr = r + dr
                    nc = c + dc
                    if 0 <= nr < R and 0 <= nc < C:
                        if nums[nr][nc] == val:
                            next_paths.add((nr, nc))

            if len(next_paths) == 0:
                break
            current_paths = next_paths

    # for r in range(R):
    #     for c in range(C):
    #         x = nums[r][c]
    #         if (r, c) in visited_cells:
    #             print(CGRN + str(x) + CEND, end="")
    #         else:
    #             print(str(x), end="")
    #     print()

    res = len(visited_cells)
    return res


p1_s1 = solve1(text_sample1)
print(CWHT + "sample:", p1_s1, CEND)  # 844
assert p1_s1 == 844
print(CGRN + "puzzle:", solve1(text_p1), CEND)  # 638

p2_s1 = solve2(text_sample2)
print(CWHT + "sample:", p2_s1, CEND)  # 1,3,4,2
assert p2_s1 == "1,3,4,2"
print(CGRN + "puzzle:", solve2(text_p2), CEND)  # 6,3,2,9,5,7,8,1,4

p3_s1 = solve3(text_sample3_1)
print(CWHT + "sample:", p3_s1, CEND)  # 33
assert p3_s1 == 33
p3_s2 = solve3(text_sample3_2)
print(CWHT + "sample:", p3_s2, CEND)  # 1125
assert p3_s2 == 1125
print(CGRN + "puzzle:", solve3(text_p3), CEND)  # 153801

stop = datetime.now()
print("duration:", stop - start)
