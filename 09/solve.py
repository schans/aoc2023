#!/usr/bin/env python3

import fileinput
# counters
T = T2 = 0
R = list()

for line in fileinput.input():
    l = line.strip()
    if not l:
        continue
    R.append([int(x) for x in l.split()])


def reduce(s):
    n = list()
    for i in range(len(s)-1):
        n.append(s[i+1]-s[i])
    return n


for r in R:
    l = list()
    b = list()
    l.append(r[-1])
    b.append(r[0])

    while not all(x == 0 for x in r):
        r = reduce(r)
        l.append(r[-1])
        b.append(r[0])
    T += sum(l)
    n = 0
    for i in range(len(b)-1, 0, -1):
        n = b[i] - n
    T2 += (b[0] - n)

print(f"Tot {T} {T2}")
