#!/usr/bin/env python3

from collections import defaultdict
import fileinput
# counters
T = T2 = 0
S = set()
O = set()
R = 0
C = 0

r = 0
for line in fileinput.input():
    l = line.strip()
    if not l:
        continue

    for c, chr in enumerate(l):
        if chr == '#':
            S.add((r, c))
        elif chr == 'O':
            O.add((r, c))

    r += 1
    C = len(l)
R = r


# def dump():
#     for r in range(R):
#         for c in range(C):
#             if (r, c) in O:
#                 print("O", end="")
#             elif (r, c) in S:
#                 print("#", end="")
#             else:
#                 print(".", end="")
#         print()


def move_up():
    global O, S
    NO = set()
    for c in range(C):
        max_to = 0
        for r in range(R):
            if (r, c) in O:
                if r > max_to:
                    # move
                    NO.add((max_to, c))
                    max_to += 1
                    continue
                else:
                    NO.add((r, c))
                    max_to = r + 1
                    continue
            if (r, c) in S:
                max_to = r+1
                continue
    O = NO.copy()


def move_down():
    global O, S
    NO = set()
    for c in range(C):
        max_to = R-1
        for r in range(R-1, -1, -1):
            if (r, c) in O:
                if r < max_to:
                    # move
                    NO.add((max_to, c))
                    max_to -= 1
                    continue
                else:
                    NO.add((r, c))
                    max_to = r - 1
                    continue
            if (r, c) in S:
                max_to = r-1
                continue
    O = NO.copy()


def move_right():
    global O, S
    NO = set()
    for r in range(R):
        max_to = C-1
        for c in range(C-1, -1, -1):
            if (r, c) in O:
                if c < max_to:
                    # move
                    NO.add((r, max_to))
                    max_to -= 1
                    continue
                else:
                    NO.add((r, c))
                    max_to = c - 1
                    continue
            if (r, c) in S:
                max_to = c-1
                continue
    O = NO.copy()


def move_left():
    global O, S
    NO = set()
    for r in range(R):
        max_to = 0
        for c in range(C):
            if (r, c) in O:
                if c > max_to:
                    # move
                    NO.add((r, max_to))
                    max_to += 1
                    continue
                else:
                    NO.add((r, c))
                    max_to = c + 1
                    continue
            if (r, c) in S:
                max_to = c+1
                continue

    O = NO.copy()


move_up()
for (r, _) in O:
    T += R - r

# complete first iteration
move_left()
move_down()
move_right()

# some iterations to settle in cycle
for i in range(1, 1000):
    move_up()
    move_left()
    move_down()
    move_right()

# find "needle" value at this point
needle = 0
for (r, _) in O:
    needle += R - r
# print("using needle 1000", needle)

# iterate till needle is found
cycle = list()
for i in range(1000):
    move_up()
    move_left()
    move_down()
    move_right()
    load = 0
    for (r, _) in O:
        load += R - r
    cycle.append(load)
    if load == needle:
        # print("load", i+1, load, len(cycle))
        break

# find offset
offset = 0
for i in range(len(cycle)):
    if cycle[1000 % len(cycle) + i] == needle:
        # print("found offset", i)
        offset = i
        break

# lookup value in cycle
ITERS = 1_000_000_000
T2 = cycle[ITERS % len(cycle) + offset]

print(f"Tot {T} {T2}")
