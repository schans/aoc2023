#!/usr/bin/env python3

import fileinput

# counters
T = T2 = 0
O = set()
L = set()
C = set()
I = dict()

F = set()

# rmin = rmax = cmin = cmax = 0
# rmin2 = rmax2 = cmin2 = cmax2 = 0

r = c = 0
r2 = c2 = 0
for line in fileinput.input():
    l = line.strip()
    if not l:
        continue

    (d, n, clr) = l.split()
    C.add((r, c))

    n = int(n)

    I[(r, c)] = (d, n)

    if d == 'U':
        L.add((r-n+1, c, r+1, c))
        r -= n
    elif d == 'D':
        L.add((r, c, r+n, c))
        r += n
    elif d == 'L':
        L.add((r, c-n+1, r, c+1))
        c -= n
    elif d == 'R':
        L.add((r, c, r, c+n))
        c += n
    else:
        assert False, f"unknown dir {d}"

    # part 2
    # convert to base 10
    n = int(clr[2:-2], 16)

    # 0 means R, 1 means D, 2 means L, and 3 means U.
    if clr[-2] == '0':
        d = 'R'
    if clr[-2] == '1':
        d = 'D'
    if clr[-2] == '2':
        d = 'L'
    if clr[-2] == '3':
        d = 'U'
    print(clr, "=", d, n)


def dump(L, P, F):
    rmin = cmin = 10000000
    rmax = cmax = 0
    for (r1, c1, r2, c2) in L:
        # print(f"{r1},{c1} - {r2},{c2}")
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
                # print(f"{r1}<={r}<{r2} {c1} <= {c} < {c2}")
                if r == r1 == r2 and c1 <= c < c2:
                    print("#", end="")
                    f = True
                if r1 <= r < r2 and c == c1 == c2:
                    print("#", end="")
                    f = True
            if not f:
                print(".", end="")
        print()


def get_top_left(C):
    minr = 1_000_000
    for (r, _) in C:
        minr = min(r, minr)

    minc = 1_000_000
    for (r, c) in C:
        if r == minr:
            minc = min(c, minc)
    return (minr, minc)


def get_left_fill_line(cr, right_c, I, C):
    global F

    # fill inside the lines to the left
    t = 0

    print("  left fill line", cr, right_c)
    first_left = -1_000_000_000_000
    for (r, c) in C:
        if c < right_c:
            (d, n) = I[(r, c)]
            if d == "L" and r == cr:
                first_left = max(first_left, c)
            if d == "R" and r == cr:
                first_left = max(first_left, c+n)
            if d == "U" and r-n < cr < r:
                first_left = max(first_left, c)
            if d == "D" and r < cr < r+n:
                first_left = max(first_left, c)

    print("    first left", (cr, right_c), "is", first_left, "fill:", right_c - first_left - 1)
    t += right_c-first_left - 1  # inner

    for cc in range(first_left+1, right_c):
        F.add((cr, cc))
    return t


def get_left_fill(top_r, bottom_r, right_c, I, C):
    global F
    # fill inside the lines to the left
    t = 0

    print("  left fill", top_r, bottom_r, right_c)
    for cr in range(top_r+1, bottom_r):
        first_left = -1_000_000_000_000
        for (r, c) in C:
            if c < right_c:
                (d, n) = I[(r, c)]
                if d == "L" and r == cr:
                    first_left = max(first_left, c)
                if d == "R" and r == cr:
                    first_left = max(first_left, c+n)
                if d == "U" and r-n < cr < r:
                    first_left = max(first_left, c)
                if d == "D" and r < cr < r+n:
                    first_left = max(first_left, c)

        print("    first left", (cr, right_c), "is", first_left)
        t += right_c-first_left - 1  # inner

        for cc in range(first_left+1, right_c):
            F.add((cr, cc))
    return t


def round_fill(tl, I, C):
    # route is clockwise
    inside = 'R'
    t = 0
    pd = 'U'
    (r, c) = tl
    while True:
        (d, n) = I[(r, c)]

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
                t += get_left_fill(r, nr, c, I, C)
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
                t += get_left_fill(r, nr, c, I, C)

            if inside == 'L' and pd == 'L':
                # top left corner
                t += get_left_fill_line(r, c, I, C)
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
                t += get_left_fill_line(r, c, I, C)

        # move next
        print("move from", (r, c), "to", (nr, nc), n, d)
        (r, c) = (nr, nc)
        pd = d
        if (r, c) == tl:
            break

    return t


# dump(L, C)
tl = get_top_left(C)

# T = rect_fill(L, C)
print("topleft", tl, I[tl])
T = round_fill(tl, I, C)
dump(L, C, F)

print(f"Tot {T} {T2}")
