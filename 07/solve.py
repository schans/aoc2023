#!/usr/bin/env python3

import functools
import fileinput
from collections import defaultdict

# counters
T = T2 = 0

D = dict()
C = list()

CARDS = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']
CARDS2 = ['A', 'K', 'Q', 'T', '9', '8', '7', '6', '5', '4', '3', '2', 'J']

for line in fileinput.input():
    l = line.strip()
    if not l:
        continue

    (h, b) = l.split()
    b = int(b)
    D[h] = b
    C.append(h)


def get_hand_value2(h):
    p = defaultdict(int)
    for c in CARDS2[:-1]:
        p[h.count(c)] += 1

    j = h.count('J')

    if p[5]:
        return 10_000
    elif p[4] and j:
        return 10_000
    elif p[4]:
        return 1_000
    elif p[3] and p[2]:
        return 150
    elif p[3] and j == 2:
        return 10_000
    elif p[3] and j == 1:
        return 1_000
    elif p[3]:
        return 100
    elif p[2] == 2 and j:
        return 150
    elif p[2] == 2:
        return 20
    elif p[2] and j == 3:
        return 10_000
    elif p[2] and j == 2:
        return 1_000
    elif p[2] and j == 1:
        return 100
    elif p[2]:
        return 10
    elif j == 5 or j == 4:
        return 10_000
    elif j == 3:
        return 1_000
    elif j == 2:
        return 100
    elif j == 1:
        return 10
    else:
        return 1


def get_hand_value(h):
    p = defaultdict(int)
    for c in CARDS:
        p[h.count(c)] += 1

    if p[5]:
        return 10_000
    elif p[4]:
        return 1_000
    elif p[3] and p[2]:
        return 150
    elif p[3]:
        return 100
    elif p[2] == 2:
        return 20
    elif p[2]:
        return 10
    else:
        return 1


def compare2(h1, h2):
    v1 = get_hand_value2(h1)
    v2 = get_hand_value2(h2)
    if v1 < v2:
        return -1
    elif v1 > v2:
        return 1
    else:
        for c in range(len(h1)):
            if h1[c] == h2[c]:
                continue
            if CARDS2.index(h1[c]) > CARDS2.index(h2[c]):
                return -1
            else:
                return 1
        return 0


def compare(h1, h2):
    v1 = get_hand_value(h1)
    v2 = get_hand_value(h2)
    if v1 < v2:
        return -1
    elif v1 > v2:
        return 1
    else:
        for c in range(len(h1)):
            if h1[c] == h2[c]:
                continue
            if CARDS.index(h1[c]) > CARDS.index(h2[c]):
                return -1
            else:
                return 1
        return 0


CS = sorted(C, key=functools.cmp_to_key(compare))
CS2 = sorted(C, key=functools.cmp_to_key(compare2))

for i, c in enumerate(CS):
    T += (i+1) * D[c]

for i, c in enumerate(CS2):
    T2 += (i+1) * D[c]


print(f"Tot {T} {T2}")
