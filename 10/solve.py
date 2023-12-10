#!/usr/bin/env python3

import fileinput
from typing import Tuple

# counters
T = T2 = 0
G = set()
L = list()
LS = set()
O = set()
I = set()


DIRS = ((-1, 0), (0, 1), (1, 0),  (0, -1), )

G = [l.strip() for l in fileinput.input()]
H = len(G)
W = len(G[0])


def get_start() -> Tuple[int, int]:
    for y in range(H):
        for x in range(W):
            if G[y][x] == 'S':
                return (x, y)

    return (-1, -1)


start = get_start()

# part 1
for dx, dy in DIRS:
    (x, y) = start
    loop = False
    L = list()
    LS = set()
    L.append(start)
    LS.add(start)
    while True:
        x = x + dx
        y = y + dy
        if not (0 <= x < W and 0 <= y < H):
            # out of grid
            break
        n = G[y][x]

        L.append((x, y))  # start in here twice for loop
        LS.add((x, y))

        if (x, y) == start:
            # looped
            loop = True
            break

        if n == '.':
            break
        elif n == '|':
            if dx == 0 and dy == 1:
                dx, dy = 0, 1
            elif dx == 0 and dy == -1:
                dx, dy = 0, -1
            else:
                break
        elif n == '-':
            if dx == 1 and dy == 0:
                dx, dy = 1, 0
            elif dx == -1 and dy == 0:
                dx, dy = -1, 0
            else:
                break
        elif n == 'L':
            if dx == 0 and dy == 1:
                dx, dy = 1, 0
            elif dx == -1 and dy == 0:
                dx, dy = 0, -1
            else:
                break
        elif n == 'J':
            if dx == 1 and dy == 0:
                dx, dy = 0, -1
            elif dx == 0 and dy == 1:
                dx, dy = -1, 0
            else:
                break
        elif n == '7':
            if dx == 1 and dy == 0:
                dx, dy = 0, 1
            elif dx == 0 and dy == -1:
                dx, dy = -1, 0
            else:
                break
        elif n == 'F':
            if dx == 0 and dy == -1:
                dx, dy = 1, 0
            elif dx == -1 and dy == 0:
                dx, dy = 0, 1
            else:
                break

    if loop:
        break

T = len(LS) // 2

# part 2

# trace loop and mark I vs O
prev = None
for x, y in L:
    if not prev:
        prev = (x, y)
        continue

    dx = x - prev[0]
    dy = y - prev[1]

    if dx == 1:
        # right
        if y > 0 and (x, y-1) not in LS:
            O.add((x, y-1))
        if y + 1 < H and (x, y+1) not in LS:
            I.add((x, y+1))
        if x+1 < W and (x+1, y) not in LS:
            if G[y][x] == '7':
                O.add((x+1, y))
            if G[y][x] == 'J':
                I.add((x+1, y))
    elif dx == -1:
        # left
        if y > 0 and (x, y-1) not in LS:
            I.add((x, y-1))
        if y + 1 < H and (x, y+1) not in LS:
            O.add((x, y+1))
        if x > 0 and (x-1, y) not in LS:
            if G[y][x] == 'F':
                I.add((x-1, y))
            if G[y][x] == 'L':
                O.add((x-1, y))
    elif dy == 1:
        # down
        if x > 0 and (x-1, y) not in LS:
            I.add((x-1, y))
        if x+1 < W and (x+1, y) not in LS:
            O.add((x+1, y))
        if y+1 < H and (x, y+1) not in LS:
            if G[y][x] == 'L':
                I.add((x, y+1))
            if G[y][x] == 'J':
                O.add((x, y+1))
    elif dy == -1:
        # up
        if x > 0 and (x-1, y) not in LS:
            O.add((x-1, y))
        if x+1 < W and (x+1, y) not in LS:
            I.add((x+1, y))
        if y > 0 and (x, y-1) not in LS:
            if G[y][x] == 'F':
                O.add((x, y-1))
            if G[y][x] == '7':
                I.add((x, y-1))
        pass
    else:
        assert False

    prev = (x, y)

# Fill
po = -1
pi = -1
while True:
    if len(O) == po and len(I) == pi:
        # no more changes
        break

    po = len(O)
    pi = len(I)

    for y in range(H):
        for x in range(W):
            if (x, y) in LS or (x, y) in O or (x, y) in I:
                continue

            for dx, dy in DIRS:
                ddx = x + dx
                ddy = y + dy
                if (ddx, ddy) in O:
                    # next to outer
                    O.add((x, y))
                    break
                if (ddx, ddy) in I:
                    # next to inner
                    I.add((x, y))
                    break


print(f"Tot {T} ({len(LS)}) I:{len(I)} O:{len(O)}")
