from datetime import datetime
from itertools import combinations, permutations
# import pyperclip

CWHT = '\033[97m'
CGRN = '\033[92m'
CEND = '\033[0m'

start = datetime.now()

quest = 'hub_q01'

text_sample1 = open(quest + '_sample_p1.txt').read()
text_p1 = open(quest + '_puzzle_p1.txt').read()

text_sample2 = open(quest + '_sample_p2.txt').read()
text_p2 = open(quest + '_puzzle_p2.txt').read()

text_sample3_1 = open(quest + '_sample_p3_1.txt').read()
text_sample3_2 = open(quest + '_sample_p3_2.txt').read()
text_sample3_3 = open(quest + '_sample_p3_3.txt').read()
text_p3 = open(quest + '_puzzle_p3.txt').read()


def solve1(text):
    nails = []
    behaviors = []
    tokens, directions = text.split('\n\n')
    for t in tokens.split('\n'):
        nails.append([x for x in t])
    for d in directions.split('\n'):
        behaviors.append([x for x in d])

    slot_count = len(behaviors)

    R = len(nails)
    C = len(nails[0])
    print(R, C)

    res = 0
    for i in range(slot_count):
        slot_num = i + 1
        behavior = behaviors[i]
        r = 0
        c = i * 2
        is_final = False
        while not is_final:
            print(r, c)
            if nails[r][c] == "*":
                d = behavior.pop(0)
                if d == "R":
                    if c == C - 1:
                        c -= 1
                    else:
                        c += 1
                    r += 1
                elif d == "L":
                    if c == 0:
                        c += 1
                    else:
                        c -= 1
                    r += 1
                else:
                    assert False, "unknown direction " + d
            elif nails[r][c] == ".":
                # fall down
                r += 1
            else:
                assert False, "unknown nail " + nails[r][c]
            if r == R and c % 2 == 0:
                is_final = True

        assert c % 2 == 0
        current_slot = c // 2 + 1
        res += max(0,(current_slot * 2) - slot_num)

    return res

def simulate(i, nails, R, C, behavior):
    slot_num = i + 1
    r = 0
    c = i * 2
    is_final = False
    while not is_final:
        # print(r, c)
        if nails[r][c] == "*":
            d = behavior.pop(0)
            if d == "R":
                if c == C - 1:
                    c -= 1
                else:
                    c += 1
                r += 1
            elif d == "L":
                if c == 0:
                    c += 1
                else:
                    c -= 1
                r += 1
            else:
                assert False, "unknown direction " + d
        elif nails[r][c] == ".":
            # fall down
            r += 1
        else:
            assert False, "unknown nail " + nails[r][c]
        if r == R and c % 2 == 0:
            is_final = True

    assert c % 2 == 0
    current_slot = c // 2 + 1
    win = max(0, (current_slot * 2) - slot_num)
    # print(slot_num, current_slot, win)
    return win


def solve2(text):
    nails = []
    behaviors = []
    tokens, directions = text.split('\n\n')
    for t in tokens.split('\n'):
        nails.append([x for x in t])
    for d in directions.split('\n'):
        behaviors.append([x for x in d])

    # print(nails)
    # print(behaviors)

    # print(slot_count)

    R = len(nails)
    C = len(nails[0])
    # print(R, C)

    slot_count = (C + 1) // 2

    res = 0
    for b in behaviors:
        best = None
        for i in range(slot_count):
            score = simulate(i, nails, R, C, b[:])
            # print(i, score)
            if best is None or score > best:
                best = score
        res += best
        # assert False

    return res


def solve3(text):
    nails = []
    behaviors = []
    tokens, directions = text.split('\n\n')
    for t in tokens.split('\n'):
        nails.append([x for x in t])
    for d in directions.split('\n'):
        behaviors.append([x for x in d])

    # print(nails)
    # print(behaviors)

    # print(slot_count)

    R = len(nails)
    C = len(nails[0])
    # print(R, C)

    slot_count = (C + 1) // 2

    all_scores = []
    for b in behaviors:
        scores = []
        for i in range(slot_count):
            score = simulate(i, nails, R, C, b[:])
            scores.append(score)
            # print(i, score)
        all_scores.append(scores)

    for scores     in all_scores:
        print(scores)
    # print(all_scores)

    assert len(behaviors) == 6

    numbers = range(slot_count)  # 1 až 20
    six_tuples = list(permutations(numbers, 6))
    max_total = None
    min_total = None
    for t in six_tuples:
        # print(t)
        total = 0
        for i in range(6):
            total += all_scores[i][t[i]]
        if max_total is None or total > max_total:
            max_total = total
        if min_total is None or total < min_total:
            min_total = total

    res = min_total, max_total
    return res


# p1_s1 = solve1(text_sample1)
# print(CWHT + "sample:", p1_s1, CEND)  #
# assert p1_s1 == 26
# print(CGRN + "puzzle:", solve1(text_p1), CEND)  # 50

# print(CGRN + "puzzle:", solve2(text_p1), CEND)  # 50

# p2_s1 = solve2(text_sample2)
# print(CWHT + "sample:", p2_s1, CEND)  #
# assert p2_s1 == 115
# print(CGRN + "puzzle:", solve2(text_p2), CEND)  # 1110

p3_s1 = solve3(text_sample3_1)
print(CWHT + "sample:", p3_s1, CEND)  #
assert p3_s1 == (13, 43)
p3_s2 = solve3(text_sample3_2)
print(CWHT + "sample:", p3_s2, CEND)  #
assert p3_s2 == (25, 66)
p3_s3 = solve3(text_sample3_3)
print(CWHT + "sample:", p3_s3, CEND)  #
assert p3_s3 == (39, 122)
print(CGRN + "puzzle:", solve3(text_p3), CEND)  #

stop = datetime.now()
print("duration:", stop - start)
