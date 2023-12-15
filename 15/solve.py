#!/usr/bin/env python3

import fileinput

from collections import defaultdict

# counters
T = 0
T2 = 0
P = list()


for line in fileinput.input():
    l = line.strip()
    if not l:
        continue

    P = l.split(',')


def get_hash(s):
    sum = 0
    for c in s:
        sum += ord(c)
        sum *= 17
        sum %= 256
    return sum


for p in P:
    T += get_hash(p)

B = defaultdict(list)
for p in P:
    if p.endswith('-'):
        label = p[:-1]
        h = get_hash(label)
        box = B[h]
        nb = list()
        for (la, le) in box:
            if la != label:
                nb.append((la, le))
        B[h] = nb

    else:
        label, lens = p.split('=')
        h = get_hash(label)
        box = B[h]
        found = False
        nb = list()
        for (la, le) in box:
            if la == label:
                found = True
                nb.append((label, lens))
            else:
                nb.append((la, le))
        if not found:
            nb.append((label, lens))
        B[h] = nb


for h, b in B.items():
    if len(b) == 0:
        continue

    for i, (label, lens) in enumerate(b, 1):
        sum = int(h) + 1
        sum *= i
        sum *= int(lens)
        T2 += sum


print(f"Tot {T} {T2}")
