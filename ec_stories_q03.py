from datetime import datetime
import re

CWHT = '\033[97m'
CGRN = '\033[92m'
CEND = '\033[0m'

start = datetime.now()

quest = 'echoes_q03'

text_sample1 = open(quest + '_sample_p1.txt').read()
text_p1 = open(quest + '_puzzle_p1.txt').read()

text_sample2_1 = open(quest + '_sample_p2_1.txt').read()
text_sample2_2 = open(quest + '_sample_p2_2.txt').read()
text_p2 = open(quest + '_puzzle_p2.txt').read()

# no sample for p3
text_p3 = open(quest + '_puzzle_p3.txt').read()


def get_all_nums(line):
    return list(map(int, re.findall(r"[+-]?\d+", line.strip())))


def move(x, y):
    r = y - 1
    c = x - 1
    if r > 0:
        r -= 1
        c += 1
    else:
        r = c
        c = 0

    return c + 1, r + 1


def solve1(text):
    P = []
    for line in text.splitlines():
        x, y = get_all_nums(line)
        P.append((x, y))

    for i in range(100):
        for e, (x, y) in enumerate(P):
            nx, ny = move(x, y)
            P[e] = (nx, ny)

    res = 0
    for x, y in P:
        res += x + (100 * y)

    return res


def solve2(text):
    P = []
    for line in text.splitlines():
        x, y = get_all_nums(line)
        P.append((x, y))

    snails_count = len(P)
    i = 0
    while True:
        on_row_1_count = 0
        for e, (x, y) in enumerate(P):
            nx, ny = move(x, y)
            P[e] = (nx, ny)
            if ny == 1:
                on_row_1_count += 1
        i += 1
        if on_row_1_count == snails_count:
            res = i
            break

    return res


def gcd_extended(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = gcd_extended(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y


def find_min_x(num, rem):
    prod = 1
    for n in num:
        prod *= n

    result = 0
    for i in range(len(num)):
        prod_i = prod // num[i]
        _, inv_i, _ = gcd_extended(prod_i, num[i])
        result += rem[i] * prod_i * inv_i

    return result % prod


def solve3(text):
    P = []
    for line in text.splitlines():
        x, y = get_all_nums(line)
        P.append((x, y))

    nums = []
    rems = []
    for x, y in P:
        offset = y - 1
        period = x + (y - 1)
        # 1,5 -> 1+4 = 5
        # 1,3 -> 1+2 = 3
        # 8,4 -> 8+3 = 11
        nums.append(period)
        rems.append(offset)

    # first is at y = 1 after o1 + k1 * p1
    # second is at y = 1 after o2 + k2 * p2
    # last is at y = 1 after on + kn * pn

    # slow solution:
    # find t where all are at y = 1
    # t = 0
    # found = False
    # while not found:
    #     t += 1
    #     found = True
    #     for offset, period in C:
    #         if (t - offset) % period != 0:
    #             found = False
    #             break
    # res = t

    # chinese remainder theorem
    res = find_min_x(nums, rems)

    return res


p1_s1 = solve1(text_sample1)
print(CWHT + "sample:", p1_s1, CEND)  # 1310
assert p1_s1 == 1310
print(CGRN + "puzzle:", solve1(text_p1), CEND)  # 3639

p2_s1 = solve2(text_sample2_1)
print(CWHT + "sample:", p2_s1, CEND)  # 14
assert p2_s1 == 14
p2_s2 = solve2(text_sample2_2)
print(CWHT + "sample:", p2_s2, CEND)  # 13659
assert p2_s2 == 13659
print(CGRN + "puzzle:", solve2(text_p2), CEND)  # 1087724

# use solve3 for p2 to check
p2_s1 = solve3(text_sample2_1)
print(CWHT + "sample:", p2_s1, CEND)  # 14
assert p2_s1 == 14
p2_s2 = solve3(text_sample2_2)
print(CWHT + "sample:", p2_s2, CEND)  # 13659
assert p2_s2 == 13659
p2_p = solve3(text_p2)
assert p2_p == 1087724
print(CWHT + "puzzle:", p2_p, CEND)  # 1087724

print(CGRN + "puzzle:", solve3(text_p3), CEND)  # 95973581860

stop = datetime.now()
print("duration:", stop - start)
