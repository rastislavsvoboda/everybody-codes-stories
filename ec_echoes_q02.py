from datetime import datetime
from dataclasses import dataclass

CWHT = '\033[97m'
CGRN = '\033[92m'
CEND = '\033[0m'

start = datetime.now()

quest = 'echoes_q02'

text_sample1_1 = open(quest + '_sample_p1_1.txt').read()
text_sample1_2 = open(quest + '_sample_p1_2.txt').read()
text_p1 = open(quest + '_puzzle_p1.txt').read()

text_sample2 = open(quest + '_sample_p2.txt').read()
text_p2 = open(quest + '_puzzle_p2.txt').read()

text_sample3_1 = open(quest + '_sample_p3_1.txt').read()
text_sample3_2 = open(quest + '_sample_p3_2.txt').read()
text_p3 = open(quest + '_puzzle_p3.txt').read()


@dataclass
class Node:
    id: int
    value: int
    char: str


class Tree:
    def __init__(self, node=None):
        self.val = node
        self.left = None
        self.right = None

    def add(self, node):
        if self.val is None:
            self.val = node
        else:
            self.place(node)

    def place(self, node):
        if node.value < self.val.value:
            if self.left is None:
                self.left = Tree(node)
            else:
                self.left.place(node)
        elif node.value > self.val.value:
            if self.right is None:
                self.right = Tree(node)
            else:
                self.right.place(node)
        else:
            assert False

    def count_nodes(self, dict=None, level=0):
        if dict is None:
            dict = {}

        if self.val is not None:
            if level not in dict:
                dict[level] = (1, self.val.char)
            else:
                v, s = dict[level]
                dict[level] = (v + 1, s + self.val.char)

        if self.left is not None:
            self.left.count_nodes(dict, level + 1)

        if self.right is not None:
            self.right.count_nodes(dict, level + 1)

        return dict

    def find(self, id):
        if self.val is None:
            return None
        if self.val.id == id:
            return self.val
        left_res = None
        right_res = None
        if self.left is not None:
            left_res = self.left.find(id)
        if left_res is not None:
            return left_res
        if self.right is not None:
            right_res = self.right.find(id)
        return right_res

    def find_all_parents_and_trees_with_id(self, id):
        res = []
        if self.left is not None:
            if self.left.val is not None and self.left.val.id == id:
                res.append((self, self.left))
            else:
                res.extend(self.left.find_all_parents_and_trees_with_id(id))
        if self.right is not None:
            if self.right.val is not None and self.right.val.id == id:
                res.append((self, self.right))
            else:
                res.extend(self.right.find_all_parents_and_trees_with_id(id))
        return res


def solve1(text):
    R = Tree()
    L = Tree()
    for line in text.splitlines():
        cmd, idn, left, right = line.split(' ')
        assert cmd == "ADD"
        n = int(idn.split('=')[1])
        left = left.split('=')[1][1:-1]
        l_num, l_char = left.split(',')
        ln = int(l_num)
        right = right.split('=')[1][1:-1]
        r_num, r_char = right.split(',')
        rn = int(r_num)
        L.add(Node(n, ln, l_char))
        R.add(Node(n, rn, r_char))

    cnt_left = L.count_nodes()
    cnt_right = R.count_nodes()

    val_left = sorted(cnt_left.values())
    val_right = sorted(cnt_right.values())

    x_left = val_left[-1][1]
    x_right = val_right[-1][1]
    res = x_left + x_right

    return res


def solve2(text):
    R = Tree()
    L = Tree()
    for line in text.splitlines():
        cmd, *rest = line.split(' ')
        if cmd == "ADD":
            idn, left, right = rest
            n = int(idn.split('=')[1])
            left = left.split('=')[1][1:-1]
            l_num, l_char = left.split(',')
            ln = int(l_num)
            right = right.split('=')[1][1:-1]
            r_num, r_char = right.split(',')
            rn = int(r_num)
            L.add(Node(n, ln, l_char))
            R.add(Node(n, rn, r_char))
        elif cmd == "SWAP":
            n = int(rest[0])
            old_left = L.find(n)
            old_right = R.find(n)
            tmp_val = old_left.value
            tmp_char = old_left.char
            old_left.value = old_right.value
            old_left.char = old_right.char
            old_right.value = tmp_val
            old_right.char = tmp_char
        else:
            assert False

    cnt_left = L.count_nodes()
    cnt_right = R.count_nodes()

    val_left = sorted(cnt_left.values())
    val_right = sorted(cnt_right.values())

    x_left = val_left[-1][1]
    x_right = val_right[-1][1]
    res = x_left + x_right

    return res


def solve3(text):
    R = Tree()
    L = Tree()
    for line in text.splitlines():
        cmd, *rest = line.split(' ')
        if cmd == "ADD":
            idn, left, right = rest
            n = int(idn.split('=')[1])
            left = left.split('=')[1][1:-1]
            l_num, l_char = left.split(',')
            ln = int(l_num)
            right = right.split('=')[1][1:-1]
            r_num, r_char = right.split(',')
            rn = int(r_num)
            L.add(Node(n, ln, l_char))
            R.add(Node(n, rn, r_char))
        elif cmd == "SWAP":
            n = int(rest[0])
            if n == 1:
                # swap roots
                L, R = R, L
            else:
                # find parents and trees
                par_lefts = L.find_all_parents_and_trees_with_id(n)
                par_rights = R.find_all_parents_and_trees_with_id(n)

                # assign parents and trees
                if len(par_lefts) == 1 and len(par_rights) == 1:
                    # between 2 trees
                    p1, t1 = par_lefts[0]
                    p2, t2 = par_rights[0]
                elif len(par_lefts) == 2:
                    # inside left tree
                    p1, t1 = par_lefts[0]
                    p2, t2 = par_lefts[1]
                elif len(par_rights) == 2:
                    # inside right tree
                    p1, t1 = par_rights[0]
                    p2, t2 = par_rights[1]
                else:
                    assert False

                # swap trees in parents
                if p1.left is not None and p1.left == t1:
                    p1.left = t2
                elif p1.right is not None and p1.right == t1:
                    p1.right = t2
                else:
                    assert False

                if p2.left is not None and p2.left == t2:
                    p2.left = t1
                elif p2.right is not None and p2.right == t2:
                    p2.right = t1
                else:
                    assert False
        else:
            assert False

    cnt_left = L.count_nodes()
    cnt_right = R.count_nodes()

    val_left = []
    for k, v in cnt_left.items():
        val_left.append((v[0], -k, v[1]))

    val_left.sort()

    val_right = []
    for k, v in cnt_right.items():
        val_right.append((v[0], -k, v[1]))

    val_right.sort()

    x_left = val_left[-1][2]
    x_right = val_right[-1][2]
    res = x_left + x_right

    return res


p1_s1 = solve1(text_sample1_1)
print(CWHT + "sample:", p1_s1, CEND)  # CFGNLK
assert p1_s1 == "CFGNLK"
p1_s2 = solve1(text_sample1_2)
print(CWHT + "sample:", p1_s2, CEND)  # EVERYBODYCODES
assert p1_s2 == "EVERYBODYCODES"
print(CGRN + "puzzle:", solve1(text_p1), CEND)  # QUACK!TLPFYXYT

p2_s1 = solve2(text_sample2)
print(CWHT + "sample:", p2_s1, CEND)  # MGFLNK
assert p2_s1 == "MGFLNK"
print(CGRN + "puzzle:", solve2(text_p2), CEND)  # QUACK!VGWZNSBMRWTLWN

p3_s1 = solve3(text_sample3_1)
print(CWHT + "sample:", p3_s1, CEND)  # DJMGL
assert p3_s1 == "DJMGL"
p3_s2 = solve3(text_sample3_2)
print(CWHT + "sample:", p3_s2, CEND)  # DJCGL
assert p3_s2 == "DJCGL"
print(CGRN + "puzzle:", solve3(text_p3), CEND)  # QUACK!SJNWHTYLZGSVBYYJMLFMJBBYNPNN

stop = datetime.now()
print("duration:", stop - start)
