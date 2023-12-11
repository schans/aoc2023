#!/usr/bin/env pypy3

import fileinput

# counters
T = T2 = 0
S = set()

G = [l.strip() for l in fileinput.input()]
C = len(G)
R = len(G[0])

for r in range(R):
    for c in range(C):
        if G[r][c] == '#':
            S.add((r, c))

re = set()
ce = set()
rs = set()
cs = set()
for s in S:
    rs.add(s[0])
    cs.add(s[1])

re = set(range(R))-rs
ce = set(range(C))-cs


def expand(re, ce, n, ss):
    # rows
    ns = set()
    td = set()
    for i, r in enumerate(sorted(re, reverse=True)):
        offset = (n-1)*(len(re) - i)
        for s in ss-td:
            if s[0] > r:
                ns.add((s[0]+offset, s[1]))
                td.add(s)
    ns.update(ss-td)
    assert len(ns) == len(ss)
    ss = ns

    # columns
    ns = set()
    td = set()
    for i, c in enumerate(sorted(ce, reverse=True)):
        offset = (n-1)*(len(ce) - i)
        for s in ss-td:
            if s[1] > c:
                ns.add((s[0], s[1]+offset))
                td.add(s)
    ns.update(ss-td)
    assert len(ns) == len(ss)

    return ns


def dist(S):
    tot = 0
    for s in S:
        for t in S:
            tot += abs(s[0]-t[0])+abs(s[1]-t[1])
    return tot // 2


T = dist(expand(re, ce, 2, S))
T2 = dist(expand(re, ce, 1_000_000, S))

print(f"Tot {T} {T2}")
