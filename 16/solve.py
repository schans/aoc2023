#!/usr/bin/env python3

import fileinput
from collections import deque

# counters
T = T2 = 0

G = [[c for c in l.strip()] for l in fileinput.input()]
R = len(G)
C = len(G[0])


def get_occ(start):
    global G

    seen = set()
    seen.add(start)

    occ = set()

    q = deque()
    q.append(start)

    while len(q):
        (p, d) = q.popleft()

        np = (p[0] + d[0], p[1] + d[1])

        # out of grid
        if not (0 <= np[0] < R) or not (0 <= np[1] < C):
            continue

        if (np, d) in seen:
            continue
        seen .add((np, d))
        occ.add(np)

        if G[np[0]][np[1]] == '.':
            q.append((np, d))
        elif G[np[0]][np[1]] == '-':
            if d[1] == 0:
                # split
                q.append((np, (0, -1)))
                q.append((np, (0, 1)))
            else:
                q.append((np, d))
        elif G[np[0]][np[1]] == '|':
            if d[0] == 0:
                q.append((np, (-1, 0)))
                q.append((np, (1, 0)))
                # split
            else:
                q.append((np, d))
            pass
        elif G[np[0]][np[1]] == '/':
            if d == (1, 0):
                q.append((np, (0, -1)))
            elif d == (-1, 0):
                q.append((np, (0, 1)))
            elif d == (0, 1):
                q.append((np, (-1, 0)))
            elif d == (0, -1):
                q.append((np, (1, 0)))

        elif G[np[0]][np[1]] == '\\':
            if d == (1, 0):
                q.append((np, (0, 1)))
            elif d == (-1, 0):
                q.append((np, (0, -1)))
            elif d == (0, 1):
                q.append((np, (1, 0)))
            elif d == (0, -1):
                q.append((np, (-1, 0)))

    return len(occ)


# part 1
T = get_occ(((0, -1), (0, 1)))

# part 2
m = 0
for r in range(R):
    m = max(m, get_occ(((r, -1), (0, 1))))
for r in range(R):
    m = max(m, get_occ(((r, C), (0, -1))))
for c in range(C):
    m = max(m, get_occ(((-1, c), (1, 0))))
for c in range(C):
    m = max(m, get_occ(((R, c), (-1, 0))))
T2 = m

print(f"Tot {T} {T2}")
