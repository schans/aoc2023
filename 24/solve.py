#!/usr/bin/env python3

import sympy
import fileinput

# counters
T = 0
T2 = 0

L = list()

# (bmin, bmax) = (7, 27)
(bmin, bmax) = (200000000000000, 400000000000000)

for line in fileinput.input():
    l = line.strip()
    if not l:
        continue

    l = l.replace(' @', ',')
    L.append([int(x) for x in l.replace(' @', ',').split(',')])


# part 1, manual solve
"""
y = a x + b
a = vy / vx
b = y - ax
"""
for i in range(len(L)):
    (x1, y1, _, vx1, vy1, _) = L[i]
    a1 = vy1 / vx1
    b1 = y1 - a1 * x1
    # print(f"y = {a1} x + {b1}")
    for j in range(i, len(L)):
        (x2, y2, _, vx2, vy2, _) = L[j]
        a2 = vy2 / vx2
        b2 = y2 - a2 * x2

        # skip parallel
        if a1 == a2:
            continue

        # lines cross
        x = (b2 - b1) / (a1 - a2)
        y = a1 * x + b1

        # past/future
        f1 = f2 = False
        if (x - x1 > 0 and vx1 > 0) or (x - x1 < 0 and vx1 < 0):
            f1 = True
        if (x - x2 > 0 and vx2 > 0) or (x - x2 < 0 and vx2 < 0):
            f2 = True

        if bmin < x <= bmax and bmin < y <= bmax and f1 and f2:
            T += 1

# part 2
# use sympy to solve equations
"""
# rock
x = rvx * t + rx
y = rvy * t + ry
z = rvz * t + rz

# hailstone
x = vx * t + sx
y = vy * t + sy
z = vz * t + sz

x - sx = t * (vx - rvx)
t = (x - sx) / (vx - rvx)

t = (rx - sx) / (vx - rvx) = (ry - sy) / (vy - rvy) 
t = (rx - sx) / (vx - rvx) = (rz - sz) / (vz - rvz) 

(rx - sx) * (vy - rvy) = (ry - sy) * (vx - rvx)
(rx - sx) * (vz - rvz) = (rz - sz) * (vx - rvx)
"""

# setup rock symbols
rx, ry, rz, rvx, rvy, rvz = sympy.symbols("rx, ry, rz, rvx, rvy, rvz")
eqs = list()
for sx, sy, sz, vx, vy, vz in L:
    eqs.append((rx - sx) * (vy - rvy) - (ry - sy) * (vx - rvx))
    eqs.append((rx - sx) * (vz - rvz) - (rz - sz) * (vx - rvx))

ans = sympy.solve(eqs).pop()
T2 = ans[rx]+ans[ry]+ans[rz]

print(f"Tot {T} {T2}")
