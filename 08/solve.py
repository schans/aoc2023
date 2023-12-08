#!/usr/bin/env python3

import fileinput

import re

# counters
T = T2 = 0
I = list()
S = dict()

A = set()

for line in fileinput.input():
    l = line.strip()
    if not l:
        continue

    if not I:
        I = list(l)
        continue

    [c, l, r] = re.findall("\\w{3}", l)
    S[c] = (l, r)
    if c.endswith("A"):
        A.add(c)

L = len(I)

# part 1
c = "AAA"
while True:
    i = I[T % L]
    if i == 'L':
        c = S[c][0]
    else:
        c = S[c][1]

    T += 1
    if c == "ZZZ":
        break


def factors(zs):
    f = list()
    for k in range(1, min(zs) + 1):
        if all(z % k == 0 for z in zs):
            f.append(k)
    return f


Z = list()
for a in A:
    # find cycle for a to z
    seen = dict()
    k = 0
    K = list()

    while True:
        m = k % L
        i = I[m]

        if (m, a) in seen:
            Z.append(K[0])
            break
        seen[(m, a)] = k

        if i == 'L':
            a = S[a][0]
        else:
            a = S[a][1]

        k += 1
        if a.endswith("Z"):
            K.append(k)


# ans is all factors multiplied by all reduced values multiplied
T2 = 1
for k in factors(Z):
    T2 *= k
    for i in range(len(Z)):
        Z[i] = Z[i] // k

for z in Z:
    T2 *= z

print(f"Tot {T} {T2}")
