#!/usr/bin/env python3

import fileinput
from pprint import pprint
from copy import deepcopy

# counters
T = T2 = 0
L = list()


GS = list()
g = list()
for line in fileinput.input():
    l = line.strip()
    if not l:
        GS.append(g)
        g = list()
        continue

    g.append([c for c in l])
GS.append(g)


def row_mirror(g):
    s = len(g)
    pivots = list()
    for i in range(s-1):
        if g[i] == g[i+1]:
            pivots.append(i)

    found = list()
    for p in pivots:
        mirror = True
        for i in range(s):
            l = p - i
            r = p + i + 1
            if l < 0 or r < 0 or l >= s or r >= s:
                break
            if g[l] != g[r]:
                mirror = False
                break
        if mirror:
            found.append(p+1)

    return found


for g in GS:
    R = len(g)
    C = len(g[0])

    c_mirror = row_mirror(list(zip(*g)))
    r_mirror = row_mirror(g)

    # check if dataset is nice
    assert len(c_mirror) < 2
    assert len(r_mirror) < 2

    # part 1
    if len(c_mirror):
        T += c_mirror[0]
    if len(r_mirror):
        T += 100 * r_mirror[0]

    # part 2
    for r in range(R):
        for c in range(C):
            # flipped grid
            ng = deepcopy(g)
            if ng[r][c] == '.':
                ng[r][c] = '#'
            else:
                ng[r][c] = '.'

            c_set = set(row_mirror(list(zip(*ng))))
            r_set = set(row_mirror(ng))
            assert len(c_set) < 3
            assert len(r_set) < 3

            # remove old mirror lines
            c_set -= set(c_mirror)
            r_set -= set(r_mirror)

            # check if dataset is nice
            assert len(c_set) < 2, (c_mirror, c_set)
            assert len(r_set) < 2

            cm = rm = 0
            if len(c_set):
                cm = c_set.pop()
            if len(r_set):
                rm = r_set.pop()

            if (rm != r_mirror or cm != c_mirror) and (cm + rm) > 0:
                if rm != r_mirror:
                    T2 += 100 * rm
                if cm != c_mirror:
                    T2 += cm

# correct for double counts
T2 //= 2
print(f"Tot {T} {T2}")
