#!/usr/bin/env python3

import fileinput

# counters
T = T2 = 0
# O = set()
C = set()
C2 = set()
I = dict()
I2 = dict()


r = c = 0
r2 = c2 = 0
for line in fileinput.input():
    l = line.strip()
    if not l:
        continue

    # part 1
    (d, n, clr) = l.split()
    n = int(n)
    I[(r, c)] = (d, n)
    C.add((r, c))

    if d == 'U':
        r -= n
    elif d == 'D':
        r += n
    elif d == 'L':
        c -= n
    elif d == 'R':
        c += n
    else:
        assert False, f"unknown dir {d}"

    # part 2

    # 0 means R, 1 means D, 2 means L, and 3 means U.
    if clr[-2] == '0':
        d2 = 'R'
    elif clr[-2] == '1':
        d2 = 'D'
    elif clr[-2] == '2':
        d2 = 'L'
    elif clr[-2] == '3':
        d2 = 'U'
    else:
        assert False, f"unknown dir {clr[-2]}"

    # convert to base 10
    n2 = int(clr[2:-2], 16)
    I2[(r2, c2)] = (d2, n2)
    C2.add((r2, c2))

    if d2 == 'U':
        r2 -= n2
    elif d2 == 'D':
        r2 += n2
    elif d2 == 'L':
        c2 -= n2
    elif d2 == 'R':
        c2 += n2
    else:
        assert False, f"unknown dir {d}"


def dump(L, P):
    rmin = cmin = 10000000
    rmax = cmax = 0
    for (r1, c1, r2, c2) in L:
        rmin = min(rmin, r1)
        rmax = max(rmax, r2)
        cmin = min(cmin, c1)
        cmax = max(cmax, c2)

    print((rmin, cmin), (rmax, cmax))

    for r in range(rmin, rmax):
        for c in range(cmin, cmax):
            if (r, c) in F:
                print(" ", end="")
                continue
            if (r, c) in C:
                print("+", end="")
                continue
            f = False
            for (r1, c1, r2, c2) in L:
                if r == r1 == r2 and c1 <= c < c2:
                    print("#", end="")
                    f = True
                if r1 <= r < r2 and c == c1 == c2:
                    print("#", end="")
                    f = True
            if not f:
                print(".", end="")
        print()


def get_top_left(points):
    minr = 1_000_000_000
    for (r, _) in points:
        minr = min(r, minr)

    minc = 1_000_000_000
    for (r, c) in points:
        if r == minr:
            minc = min(c, minc)
    return (minr, minc)


def get_left_fill_line(cr, right_c, lines, points):
    # fill inside the lines to the left
    t = 0

    first_left = -1_000_000_000_000
    for (r, c) in points:
        if c < right_c:
            (d, n) = lines[(r, c)]
            if d == "L" and r == cr:
                first_left = max(first_left, c)
            if d == "R" and r == cr:
                first_left = max(first_left, c+n)
            if d == "U" and r-n < cr < r:
                first_left = max(first_left, c)
            if d == "D" and r < cr < r+n:
                first_left = max(first_left, c)

    # print("    first left", (cr, right_c), "is", first_left, "fill:", right_c - first_left - 1)
    t += right_c-first_left - 1  # inner
    return t


def get_left_fill(top_r, bottom_r, right_c, lines, points):
    # fill inside the lines to the left
    t = 0

    # print("  left fill", top_r, bottom_r, right_c)
    # very slow.. can be optimized be finding next point1
    for cr in range(top_r+1, bottom_r):
        first_left = -1_000_000_000_000
        for (r, c) in points:
            if c < right_c:
                (d, n) = lines[(r, c)]
                if d == "L" and r == cr:
                    first_left = max(first_left, c)
                if d == "R" and r == cr:
                    first_left = max(first_left, c+n)
                if d == "U" and r-n < cr < r:
                    first_left = max(first_left, c)
                if d == "D" and r < cr < r+n:
                    first_left = max(first_left, c)

        # print("    first left", (cr, right_c), "is", first_left)
        t += right_c-first_left - 1  # inner
    return t


def round_fill(tl, lines, points):
    # route is clockwise
    inside = 'R'
    t = 0
    pd = 'U'
    (r, c) = tl
    while True:
        (d, n) = lines[(r, c)]

        if d == 'U':
            nr = r - n
            nc = c
            t += n
            if pd == 'R':
                if inside == 'D':
                    inside = 'R'
                else:
                    inside = 'L'
            if pd == 'L':
                if inside == 'U':
                    inside = 'R'
                else:
                    inside = 'L'
            if inside == 'L':
                t += get_left_fill(r, nr, c, lines, points)
        elif d == 'D':
            nr = r + n
            nc = c
            t += n
            if pd == 'R':
                if inside == 'D':
                    inside = 'L'
                else:
                    inside = 'R'
            if pd == 'L':
                if inside == 'U':
                    inside = 'L'
                else:
                    inside = 'R'
            if inside == 'L':
                t += get_left_fill(r, nr, c, lines, points)

            if inside == 'L' and pd == 'L':
                # top left corner
                t += get_left_fill_line(r, c, lines, points)
        elif d == 'L':
            nr = r
            nc = c - n
            t += n
            if pd == 'U':
                if inside == 'L':
                    inside = 'D'
                else:
                    inside = 'U'
            if pd == 'D':
                if inside == 'R':
                    inside = 'D'
                else:
                    inside = 'U'
        elif d == 'R':
            nr = r
            nc = c + n
            t += n
            if pd == 'U':
                if inside == 'L':
                    inside = 'U'
                else:
                    inside = 'D'
            if pd == 'D':
                if inside == 'R':
                    inside = 'U'
                else:
                    inside = 'D'
            if inside == 'D' and pd == 'D':
                # bottom left corner
                t += get_left_fill_line(r, c, lines, points)

        # move next
        # print("move from", (r, c), "to", (nr, nc), n, d)
        (r, c) = (nr, nc)
        pd = d
        if (r, c) == tl:
            break

    return t


# part 1
tl = get_top_left(C)
T = round_fill(tl, I, C)

# part 2
tl = get_top_left(C2)
T2 = round_fill(tl, I2, C2)

print(f"Tot {T} {T2}")
