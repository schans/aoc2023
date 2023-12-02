#!/usr/bin/env python3

import fileinput

# counters
T = 0
T2 = 0
D = []
K = 1

# 12 red cubes, 13 green cubes, and 14 blue cubes
R = 12
G = 13
B = 14

for line in fileinput.input():
    l = line.strip()
    if not l:
        continue

    p = True
    ms = [0] * 3
    draws = l.split(':')[1].split(';')
    for draw in draws:
        draw = draw.strip()
        r = g = b = 0
        for cs in draw.split(','):
            c = cs.split()
            if c[1] == 'red':
                r = int(c[0])
            elif c[1] == 'green':
                g = int(c[0])
            elif c[1] == 'blue':
                b = int(c[0])

        ms[0] = max(r, ms[0])
        ms[1] = max(g, ms[1])
        ms[2] = max(b, ms[2])

    if ms[0] <= R and ms[1] <= G and ms[2] <= B:
        T += K
    T2 += ms[0] * ms[1] * ms[2]
    K += 1

print(f"Tot {T} {T2}")
