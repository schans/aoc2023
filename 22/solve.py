#!/usr/bin/env python3

import fileinput

# counters
T = 0
T2 = 0

B = list()
C = set()

for line in fileinput.input():
    l = line.strip()
    if not l:
        continue

    (p1, p2) = l.split('~')
    p1 = tuple(int(x) for x in p1.split(','))
    p2 = tuple(int(x)+1 for x in p2.split(','))  # exclusive right
    B.append((p1, p2))
    if p1[2] > p2[2]:
        print(p1, p2)


def can_move_down(b, S, ignore=None):
    ((x1, y1, z1), (x2, y2, z2)) = b

    # ground
    if z1 == 1:
        return False

    for s in S:
        if s == ignore:
            continue
        ((sx1, sy1, sz1), (sx2, sy2, sz2)) = s
        # touching ?
        if z1 == sz2 and max(x1, sx1) - min(x2, sx2) < 0 and max(y1, sy1) - min(y2, sy2) < 0:
            return False

    return True


def move_down(b, S):
    ((x1, y1, z1), (x2, y2, z2)) = b
    nb = b
    moved = False
    while can_move_down(nb, S):
        z1 -= 1
        z2 -= 1
        nb = ((x1, y1, z1), (x2, y2, z2))
        moved = True
    return nb, moved


# settle down
B = sorted(B, key=lambda x: x[0][2], reverse=False)
S = list()
for b in B:
    bn, _ = move_down(b, S)
    S.append(bn)

# part 1
for i in range(len(S)):
    safe = True
    # check block above
    for j in range(i, len(S)):
        if can_move_down(S[j], S, S[i]):
            safe = False
            break
    if safe:
        T += 1

# part 2
for s in S:
    moves = 0
    NS = S.copy()
    NS.remove(s)
    NNS = list()
    for b in NS:
        bn, moved = move_down(b, NNS)
        NNS.append(bn)
        if moved:
            moves += 1
    T2 += moves

print(f"Tot {T} {T2}")
