#!/usr/bin/env python3

from collections import deque
import fileinput
from copy import deepcopy
from heapq import heappop, heappush

# counters
T = T2 = 0

W = dict()
WG = dict()

for line in fileinput.input():
    l = line.strip()
    if not l:
        continue
    f, tl = l.split(": ")
    W[f] = set(x for x in tl.split())


# complete graph
WG = deepcopy(W)
for f, tl in W.items():
    for x in tl:
        if x in WG:
            WG[x].add(f)
        else:
            WG[x] = {f}

W = WG


def dijkstra(start, end, wires):
    q = list()
    seen = set()
    heappush(q, (0, (start, list([start]))))

    while q:
        (n, (cur, path)) = heappop(q)

        if cur == end:
            return n, path

        if cur in seen:
            continue
        seen.add(cur)

        for nl in wires[cur]:
            np = path.copy()
            np.append(nl)
            heappush(q, (n+1, (nl, np)))

    # no path found
    return -1, list()


def count_connected(start, wires):
    # dfs
    q = deque()
    seen = set()
    q.append(start)
    while q:
        l = q.pop()
        if l in seen:
            continue
        seen.add(l)
        for nl in wires[l]:
            q.append(nl)

    return len(seen)


start = list(W.keys())[0]
cuts = list()
for maxe in W.keys():
    # test two points if they are on the different groups
    if maxe == start:
        continue

    # shortest path
    maxd, maxp = dijkstra(start, maxe, W)

    # remove parts on path and check for len diff
    firsts = list()
    for i in range(maxd):
        a = maxp[i]
        b = maxp[i+1]

        CW = deepcopy(W)
        CW[a] = CW[a] - {b}
        CW[b] = CW[b] - {a}
        d, p = dijkstra(start, maxe, CW)
        if d >= maxd:
            firsts.append((a, b, d, p))

    # remove parts on path and check for len diff, again, removing 2
    seconds = list()
    for first in firsts:
        (a, b, maxd, maxp) = first
        for i in range(maxd):
            c = maxp[i]
            d = maxp[i+1]

            CW = deepcopy(W)
            CW[a] = CW[a] - {b}
            CW[b] = CW[b] - {a}
            CW[c] = CW[c] - {d}
            CW[d] = CW[d] - {c}
            dist, p = dijkstra(start, maxe, CW)
            if dist > maxd:
                seconds.append((a, b, c, d, dist, p))

    # remove parts on path and check for len diff, 3rd, check for disconnected
    candidates = set()
    for second in seconds:
        (a, b, c, d, maxd, maxp) = second
        for i in range(maxd):
            e = maxp[i]
            f = maxp[i+1]

            CW = deepcopy(W)
            CW[a] = CW[a] - {b}
            CW[b] = CW[b] - {a}
            CW[c] = CW[c] - {d}
            CW[d] = CW[d] - {c}
            CW[e] = CW[e] - {f}
            CW[f] = CW[f] - {e}
            dist, p = dijkstra(start, maxe, CW)
            if dist == -1:
                # disconnected
                candidates.add(((a, b), (c, d), (e, f)))

    if len(candidates) == 1:
        cuts = candidates.pop()
        break

# remove cuts from graph
CW = deepcopy(W)
for (a, b) in cuts:
    CW[a] = CW[a] - {b}
    CW[b] = CW[b] - {a}

c1 = count_connected(start, CW)
T = c1*(len(W)-c1)

print(f"Tot {T}")
