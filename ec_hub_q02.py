from collections import deque
from datetime import datetime

CWHT = '\033[97m'
CGRN = '\033[92m'
CEND = '\033[0m'

start = datetime.now()

quest = 'hub_q02'

text_sample1 = open(quest + '_sample_p1.txt').read()
text_p1 = open(quest + '_puzzle_p1.txt').read()

text_sample2 = open(quest + '_sample_p2.txt').read()
text_p2 = open(quest + '_puzzle_p2.txt').read()

text_p3 = open(quest + '_puzzle_p3.txt').read()


def solve1(text):
    ballons = [x for x in text.strip()]
    fluffbolds = ["R", "G", "B"]
    d = 0

    res = 0
    while len(ballons) > 0:
        res += 1
        b = ballons.pop(0)
        while len(ballons) > 0 and b == fluffbolds[d]:
            b = ballons.pop(0)
        d = (d + 1) % 3

    return res


def solve2(text, rep=100):
    part_ballons = [x for x in text.strip()]
    ballons = part_ballons * rep
    fluffbolds = ["R", "G", "B"]
    d = 0

    res = 0
    while len(ballons) > 0:
        res += 1
        cnt = len(ballons)
        current = fluffbolds[d]
        if cnt % 2 == 0 and len(ballons) > 1 and ballons[0] == current:
            middle = cnt // 2
            # remove middle baloon
            ballons = ballons[:middle] + ballons[middle + 1:]
        ballons = ballons[1:]

        d = (d + 1) % 3

    return res


def solve3_slow(text):
    part_ballons = [x for x in text.strip()]
    ballons = part_ballons * 100000
    fluffbolds = ["R", "G", "B"]
    d = 0

    res = 0
    while len(ballons) > 0:
        res += 1
        cnt = len(ballons)
        current = fluffbolds[d]
        if cnt % 2 == 0 and len(ballons) > 1 and ballons[0] == current:
            middle = cnt // 2
            # remove middle baloon
            ballons = ballons[:middle] + ballons[middle + 1:]
        ballons = ballons[1:]

        d = (d + 1) % 3

    return res


def solve3(text, rep):
    part_ballons = [x for x in text.strip()]
    ballons = part_ballons * rep
    # using deque for performance, better that arrays
    q1 = deque(ballons[:len(ballons) // 2])
    q2 = deque(ballons[len(ballons) // 2:])
    fluffbolds = ["R", "G", "B"]
    d = 0

    res = 0
    cnt = len(ballons)
    while cnt > 0:
        res += 1
        is_even = (cnt % 2 == 0)
        if cnt == 1:
            # remove last baloon
            cnt -= 1
            if len(q1) > 0:
                q1.popleft()
            elif len(q2) > 0:
                q2.popleft()
        else:
            assert len(q1) > 0
            b = q1.popleft()
            cnt -= 1
            if is_even and cnt > 0 and b == fluffbolds[d]:
                # remove middle baloon (beginning of q2)
                assert len(q2) > 0
                q2.popleft()
                cnt -= 1
            else:
                if len(q2) > 0 and cnt % 2 == 0:
                    b = q2.popleft()
                    q1.append(b)

        d = (d + 1) % 3

    return res


p1_s1 = solve1(text_sample1)
print(CWHT + "sample:", p1_s1, CEND)  # 7
assert p1_s1 == 7
print(CGRN + "puzzle:", solve1(text_p1), CEND)  # 128

p2_s1 = solve2(text_sample2, 5)
print(CWHT + "sample:", p2_s1, CEND)  # 14
assert p2_s1 == 14
print(CGRN + "puzzle:", solve2(text_p2, 100), CEND)  # 21527

assert solve3("GGBR", 5) == 14
assert solve3("BBRGGRRGBBRGGBRGBBRRBRRRBGGRRRBGBGG", 10) == 304
assert solve3("BBRGGRRGBBRGGBRGBBRRBRRRBGGRRRBGBGG", 50) == 1464
assert solve3("BBRGGRRGBBRGGBRGBBRRBRRRBGGRRRBGBGG", 100) == 2955
print(CWHT + "puzzle:", solve3(text_p2, 100), CEND)  # 21527

# no sample for p3
print(CGRN + "puzzle:", solve3(text_p3, 100000), CEND)  # 21259841

stop = datetime.now()
print("duration:", stop - start)
