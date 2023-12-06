#!/usr/bin/env python3

import fileinput

# counters
T = T2 = 0

fi = fileinput.input()
TS = [int(x) for x in next(fi).split()[1:]]
DS = [int(x) for x in next(fi).split()[1:]]


def get_diff(w, t, d) -> int:
    c = w * (t - w)
    return c - d


def find_lower(lo, hi, t, d) -> int:
    w = (lo + hi) // 2
    diff = get_diff(w, t, d)
    ndiff = get_diff(w+1, t, d)

    # stop condition
    if diff <= 0 and ndiff > 0:
        return w + 1

    if diff <= 0:
        return find_lower(w, hi, t, d)
    else:
        return find_lower(lo, w, t, d)


def find_higher(lo, hi, t, d) -> int:
    w = (lo + hi) // 2
    diff = get_diff(w, t, d)
    pdiff = get_diff(w-1, t, d)
    # stop condition
    if diff <= 0 and pdiff > 0:
        return w-1

    if diff > 0:
        return find_higher(w, hi, t, d)
    else:
        return find_higher(lo, w, t, d)


T = 1
for i in range(len(TS)):
    ways = find_higher(TS[i]//2, TS[i], TS[i], DS[i]) - find_lower(0, TS[i]//2, TS[i], DS[i]) + 1
    T *= ways

tn = int(''.join([str(i) for i in TS]))
dn = int(''.join([str(i) for i in DS]))
T2 = find_higher(tn//2, tn, tn, dn) - find_lower(0, tn//2, tn, dn) + 1

print(f"Tot {T} {T2}")
