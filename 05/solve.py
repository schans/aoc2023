#!/usr/bin/env python3

import fileinput
from collections import defaultdict
from os import sysconf_names
from pprint import pprint

import functools

# counters
T = T2 = 0
S = list()

M = defaultdict(list)
SD = dict()
SS = list()

"""
seed-to-soil map:
soil-to-fertilizer map:
fertilizer-to-water map:
water-to-light map:
light-to-temperature map:
temperature-to-humidity map:
humidity-to-location map:
"""
s = d = ""
for line in fileinput.input():
    l = line.strip()
    if not l:
        continue

    if l.startswith("seeds:"):
        S = [int(x) for x in l.split(":")[1].split()]
        continue

    if "map:" in l:
        (s, d) = l.split(" map:")[0].split("-to-")
        SD[s] = d
        SS.append(s)
        continue

    r = [int(x) for x in l.split()]
    M[s].append(r)


def get_final_dest(k):
    for t in SD:
        k = get_dest(k, M[t])
    return k


def get_dest(k, ranges):
    for (d, s, n) in ranges:
        if s <= k < s + n:
            return d + k - s
    return k


# # dump
# for i in range(0, 100):
#     n = i
#     print(f"{i:>2}", end=": ")
#
#     for t in SD:
#         n = get_dest(n, M[t])
#         print(f"{n:>2}", end=" ")
#     print()
#

# part 1
v = list()
for s in S:
    v.append(get_final_dest(s))
T = min(v)

# part 2


def get_next_part(start, left, ranges):
    dest = get_dest(start, ranges)
    ss = list()
    sn = dict()
    smax = 0
    smin = 100_000_000
    # pre process min max, right of, etc
    for (_, s, n) in ranges:
        sn[s] = n
        smax = max(smax, s)
        smin = min(smin, s)
        if s > start:
            ss.append(s)

    if len(ss):
        # got a range to the right
        smin = min(ss)
        dist = smin - start

        if left < dist:
            # full left of next range
            return (dest, left)
        else:
            # partial left
            return (dest, min(dist, left))

    else:
        # only ranges to left
        dist = smax + sn[smax] - start

        if start >= smax + sn[smax]:
            # full right of ranges
            return (dest, left)
        else:
            # partial right
            return (dest, min(left, dist))


def get_next_parts2(start, left, ranges):
    parts = list()
    while left > 0:
        p = get_next_part(start, left, ranges)
        assert p[1] > 0, p[1]
        parts.append(p)
        start += p[1]
        left -= p[1]

    assert left == 0, left
    return parts


m = 100_000_000
for i in range(0, len(S), 2):
    cur_ranges = [(S[i], S[i+1])]
    for t in SD:
        new_ranges = list()
        for r in cur_ranges:
            new_ranges.extend(get_next_parts2(r[0], r[1], M[t]))
        cur_ranges = new_ranges
    for r in cur_ranges:
        m = min(m, r[0])

T2 = m
print(f"Tot {T} {T2}")
