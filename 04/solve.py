#!/usr/bin/env python3

import fileinput
from math import floor

# counters
T = 0
T2 = 0

C = list()
CC = list()

# Card 0
C.append(1)
CC.append(0)

for line in fileinput.input():
    l = line.strip()
    if not l:
        continue

    (g, ns) = l.split(": ")
    (wns, mns) = ns.split(" | ")
    wns = set(wns.split())
    mns = set(mns.split())
    T += floor(pow(2, len(wns & mns)-1))
    C.append(len(wns & mns))
    CC.append(1)

for i, c in enumerate(C):
    for n in range(c):
        CC[i+n+1] += 1 * CC[i]

T2 = sum(CC)

print(f"Tot {T} {T2}")
