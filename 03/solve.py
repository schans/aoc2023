#!/usr/bin/env python3

import fileinput

# counters
T = T2 = 0
D = dict()
S = set()
G = set()

DIRS = ((-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1))

# grid = [l.strip() for l in fileinput.input()]
# H = len(grid)
# W = len(grid[0])

r = 0
for line in fileinput.input():
    l = line.strip()
    if not l:
        continue

    rn = False
    n = ''
    for i, c in enumerate(line):
        if c.isdigit():
            rn = True
            n += c
            continue

        if rn:
            D[(r, i - len(n))] = n
            rn = False
            n = ''

        if c != '.' and c != "\n":
            S.add((r, i))
            if c == '*':
                G.add((r, i))
    r += 1

# part 1
for (r, c), n in D.items():
    adj = False
    for i in range(len(n)):
        for (dx, dy) in DIRS:
            if (r+dx, c+dy+i) in S:
                adj = True
                break
    if adj:
        T += int(n)

# part 2
for (r, c) in G:
    A = set()
    for (dx, dy) in DIRS:
        for (i, j), n in D.items():
            if (r+dx) == i and (c+dy) >= j and (c+dy) < (j+len(n)):
                A.add((i, j))
                continue
    if len(A) == 2:
        T2 += int(D[A.pop()]) * int(D[A.pop()])

print(f"Tot {T} {T2}")
