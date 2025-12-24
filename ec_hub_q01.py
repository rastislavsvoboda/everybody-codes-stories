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


def simulate(i, nails, R, C, token):
    slot_num = i + 1
    r = 0
    c = i * 2
    is_final = False
    token_behavior = token[:]
    while not is_final:
        if nails[r][c] == "*":
            # bounce and fall down
            d = token_behavior.pop(0)
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
            # only fall down
            r += 1
        else:
            assert False, "unknown nail " + nails[r][c]
        if r == R and c % 2 == 0:
            is_final = True

    assert c % 2 == 0
    current_slot = c // 2 + 1
    win = max(0, (current_slot * 2) - slot_num)
    return win


def solve1(text):
    nails = []
    tokens = []
    nails_text, tokens_text = text.split('\n\n')
    for n in nails_text.split('\n'):
        nails.append([x for x in n])
    for t in tokens_text.split('\n'):
        tokens.append([x for x in t])

    R = len(nails)
    C = len(nails[0])

    slot_count = (C + 1) // 2

    res = 0
    for i in range(slot_count):
        token = tokens[i][:]
        res += simulate(i, nails, R, C, token)

    return res


def solve2(text):
    nails = []
    tokens = []
    nails_text, tokens_text = text.split('\n\n')
    for n in nails_text.split('\n'):
        nails.append([x for x in n])
    for t in tokens_text.split('\n'):
        tokens.append([x for x in t])

    R = len(nails)
    C = len(nails[0])

    slot_count = (C + 1) // 2

    res = 0
    for token in tokens:
        best = None
        for i in range(slot_count):
            score = simulate(i, nails, R, C, token)
            if best is None or score > best:
                best = score
        res += best

    return res


def solve3(text):
    nails = []
    tokens = []
    nails_text, tokens_text = text.split('\n\n')
    for n in nails_text.split('\n'):
        nails.append([x for x in n])
    for t in tokens_text.split('\n'):
        tokens.append([x for x in t])

    R = len(nails)
    C = len(nails[0])

    slot_count = (C + 1) // 2

    all_scores = []
    for token in tokens:
        scores = []
        for i in range(slot_count):
            score = simulate(i, nails, R, C, token)
            scores.append(score)
        all_scores.append(scores)

    tokens_count = len(tokens)

    numbers = range(slot_count)
    # depends on order, so use permutations
    six_tuples = list(permutations(numbers, tokens_count))
    max_total = None
    min_total = None
    for indices in six_tuples:
        total = 0
        for i in range(6):
            total += all_scores[i][indices[i]]
        if max_total is None or total > max_total:
            max_total = total
        if min_total is None or total < min_total:
            min_total = total

    res = str(min_total) + ' ' + str(max_total)
    return res


p1_s1 = solve1(text_sample1)
print(CWHT + "sample:", p1_s1, CEND)  # 26
assert p1_s1 == 26
print(CGRN + "puzzle:", solve1(text_p1), CEND)  # 50

p2_s1 = solve2(text_sample2)
print(CWHT + "sample:", p2_s1, CEND)  # 115
assert p2_s1 == 115
print(CGRN + "puzzle:", solve2(text_p2), CEND)  # 1110

p3_s1 = solve3(text_sample3_1)
print(CWHT + "sample:", p3_s1, CEND)  # 13 43
assert p3_s1 == "13 43"
p3_s2 = solve3(text_sample3_2)
print(CWHT + "sample:", p3_s2, CEND)  # 25 66
assert p3_s2 == "25 66"
p3_s3 = solve3(text_sample3_3)
print(CWHT + "sample:", p3_s3, CEND)  # 39 122
assert p3_s3 == "39 122"
print(CGRN + "puzzle:", solve3(text_p3), CEND)  # 36 117

stop = datetime.now()
print("duration:", stop - start)
