from datetime import datetime
from collections import deque, defaultdict
import re

# import pyperclip

CRED = '\033[91m'
CGRN = '\033[92m'
CEND = '\033[0m'

start = datetime.now()

quest = 'echoes_q01'

text_sample1 = open(quest + '_sample_p1.txt').read()
text_p1 = open(quest + '_puzzle_p1.txt').read()

text_sample2_1 = open(quest + '_sample_p2_1.txt').read()
text_sample2_2 = open(quest + '_sample_p2_2.txt').read()
text_p2 = open(quest + '_puzzle_p2.txt').read()

text_sample3_1 = open(quest + '_sample_p3_1.txt').read()
text_sample3_2 = open(quest + '_sample_p3_2.txt').read()
text_p3 = open(quest + '_puzzle_p3.txt').read()


def get_all_nums(line):
    return list(map(int, re.findall(r"[+-]?\d+", line.strip())))


def eni(n, exp, mod):
    res = []
    x = 1
    for _ in range(exp):
        x = (x * n) % mod
        res.insert(0, x)
    return res


def eni2(n, exp, mod):
    res = deque()
    x = 1
    for _ in range(exp):
        x = (x * n) % mod
        res.appendleft(x)
        if len(res) > 5:
            res.pop()
    return res


def eni2_faster(n, exp, mod):
    res = deque()
    x = 1
    # print("starting eni2_faster with n =", n, "exp =", exp, "mod =", mod)
    seen = defaultdict(list)
    found = False
    i = 0
    while i < exp:
        # print("i =", i)
        x = (x * n) % mod
        i += 1
        res.appendleft(x)
        if len(res) > 5:
            res.pop()
        state = tuple(res)
        if state in seen and not found:
            found = True
            cycle_len = i - seen[state][0]
            # print("cycle detected! len:", cycle_len, "at i =", i)
            while i < exp - cycle_len - 1:
                rest = exp - i
                cycles = rest // cycle_len
                i += cycles * cycle_len
                # i += cycle_len
            # now continue normally
            seen[state].append(i)
        else:
            seen[state].append(i)
    return res


def eni3(n, exp, mod):
    res = 0
    x = 1
    for _ in range(exp):
        x = (x * n) % mod
        res += x
    return res


def eni3_faster(n, exp, mod):
    res = 0
    x = 1
    seen = defaultdict(list)
    seen2 = defaultdict(int)
    found = False
    i = 0
    R = []
    RR = set()
    while i < exp:
        x = (x * n) % mod
        i += 1
        if x in seen and not found:
            seen2[x] += 1
            if seen2[x] == 3:
                found = True
                cycle_len = i - seen[x][0]
                assert cycle_len % 2 == 0
                cycle_len = cycle_len // 2
                # print("cycle detected! len:", cycle_len, "at i =", i)
                # seen[x].append(i)

                while i < exp - cycle_len:
                    rest = exp - i - 1
                    cycles = rest // cycle_len
                    i += cycles * cycle_len

                    for k in seen2:
                        if seen2[k] > 1:
                            seen2[k] += cycles
                    # now continue normally

            # assert False
            R.append(x)
        else:
            R.append(x)
            seen[x].append(i)
            seen2[x] += 1

        # if res in seen and not found:
        #     found = True
        #     cycle_len = i - seen[res][0]
        #     print("cycle detected! len:", cycle_len, "at i =", i)
        #     while i < exp - cycle_len - 1:
        #         rest = exp - i
        #         cycles = rest // cycle_len
        #         i += cycles * cycle_len
        #         # i += cycle_len
        #     # now continue normally
        #     seen[res].append(i)
        # else:
        #     seen[res].append(i)

    res = 0
    for k, v in seen2.items():
        res += k * v

    # res = sum(R)
    return res


def lst_to_num(lst):
    s = ''
    for x in lst:
        s += str(x)
    res = int(s)
    return res


def solve1(text):
    # func = eni(A, X, M) + eni(B, Y, M) + eni(C, Z, M)

    s1 = eni(2, 4, 5)
    assert lst_to_num(s1) == 1342

    s2 = eni(3, 5, 16)
    assert lst_to_num(s2) == 311193

    res = None
    for line in text.splitlines():
        A, B, C, X, Y, Z, M = get_all_nums(line)
        a_lst = eni(A, X, M)
        b_lst = eni(B, Y, M)
        c_lst = eni(C, Z, M)
        a_num = lst_to_num(a_lst)
        b_num = lst_to_num(b_lst)
        c_num = lst_to_num(c_lst)

        val = a_num + b_num + c_num
        if res is None or val > res:
            res = val

    return res


def solve2(text):
    # func = eni(A, X, M) + eni(B, Y, M) + eni(C, Z, M)

    # s1 = eni2(2,7,5)
    # assert lst_to_num(s1) == 34213
    # s2 = eni2(3,8,16)
    # assert lst_to_num(s2) == 111931
    # s3 = eni2(8,6,16)
    # assert lst_to_num(s3) == 0
    # s4 = eni2(8,19,16)
    # assert lst_to_num(s4) == 0
    # s5 = eni2(8,16,16)
    # assert lst_to_num(s5) == 0

    # for _i in range(1, 20):
    #     ss1 = eni2(8,_i,16)
    #     ss2 = eni2_faster(8, _i, 16)
    #     print(_i, lst_to_num(ss1), lst_to_num(ss2))

    # for _i in range(1, 30):
    #     ss1 = eni2(4,_i,11)
    #     ss2 = eni2_faster(4, _i, 11)
    #     print(_i, lst_to_num(ss1), lst_to_num(ss2))
    #
    # for _i in range(1, 30):
    #     ss1 = eni2(5,_i,11)
    #     ss2 = eni2_faster(5, _i, 11)
    #     print(_i, lst_to_num(ss1), lst_to_num(ss2))
    #
    # for _i in range(1, 30):
    #     ss1 = eni2(6,_i,11)
    #     ss2 = eni2_faster(6, _i, 11)
    #     print(_i, lst_to_num(ss1), lst_to_num(ss2))

    # assert False

    res = None
    for i, line in enumerate(text.splitlines()):
        # print(i)
        A, B, C, X, Y, Z, M = get_all_nums(line)
        a_lst = eni2_faster(A, X, M)
        b_lst = eni2_faster(B, Y, M)
        c_lst = eni2_faster(C, Z, M)
        a_num = lst_to_num(a_lst)
        b_num = lst_to_num(b_lst)
        c_num = lst_to_num(c_lst)

        val = a_num + b_num + c_num
        if res is None or val > res:
            res = val

    return res


def solve3(text):
    # s1 = eni3(2,7,5)
    # assert s1 == 19
    #
    # s2 = eni3(3,8,16)
    # assert s2 == 48
    #
    # s1 = eni3_faster(2,7,5)
    # assert s1 == 19
    #
    # s2 = eni3_faster(3,8,16)
    # assert s2 == 48

    # s3 = eni3_faster(4,3000,110)
    # assert s3 == 132000
    #
    # s4 = eni3_faster(4,14000,110)
    # assert s4 == 616000
    #
    # assert eni3_faster(6,15000,110) == 825000
    # assert eni3_faster(8,8000,120) == 240000
    assert eni3(4, 14000, 120) == 559940
    assert eni3_faster(4, 14000, 120) == 559940
    # assert eni3_faster(7,16000,120) == 640000

    # assert False
    # for _i in range(1, 20):
    #     ss1 = eni3(1,_i,10)
    #     ss2 = eni3_faster(1, _i, 10)
    #     print(_i, ss1, ss2)
    #
    # for _i in range(1, 20):
    #     ss1 = eni3(2,_i,10)
    #     ss2 = eni3_faster(2, _i, 10)
    #     print(_i, ss1, ss2)
    #
    # for _i in range(1, 20):
    #     ss1 = eni3(3,_i,10)
    #     ss2 = eni3_faster(3, _i, 10)
    #     print(_i, ss1, ss2)
    #
    #
    # assert False

    res = None
    for i, line in enumerate(text.splitlines()):
        # print(i)
        A, B, C, X, Y, Z, M = get_all_nums(line)
        a_num = eni3_faster(A, X, M)
        b_num = eni3_faster(B, Y, M)
        c_num = eni3_faster(C, Z, M)

        val = a_num + b_num + c_num
        if res is None or val > res:
            res = val

    return res


p1_s1 = solve1(text_sample1)
print(CRED + "sample:", p1_s1, CEND)  # 11611972920
assert p1_s1 == 11611972920
print(CGRN + "puzzle:", solve1(text_p1), CEND)  # 8112119159

p2_s1 = solve2(text_sample2_1)
print(CRED + "sample:", p2_s1, CEND)  # 11051340
assert p2_s1 == 11051340
p2_s2 = solve2(text_sample2_2)
print(CRED + "sample:", p2_s2, CEND)  # 1507702060886
assert p2_s2 == 1507702060886
print(CGRN + "puzzle:", solve2(text_p2), CEND)  # 130462353088217
# wrong 92697326194062

p3_s1 = solve3(text_sample3_1)
print(CRED + "sample:", p3_s1, CEND)  # 3279640
assert p3_s1 == 3279640
p3_s2 = solve3(text_sample3_2)
print(CRED + "sample:", p3_s2, CEND)  # 7276515438396
assert p3_s2 == 7276515438396
print(CGRN + "puzzle:", solve3(text_p3), CEND)  # 508850677081888

stop = datetime.now()
print("duration:", stop - start)
