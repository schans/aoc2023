#!/usr/bin/env python3

import fileinput
from heapq import heappop, heappush

# counters
T = T2 = 0

G = [[int(c) for c in l.strip()] for l in fileinput.input()]
R = len(G)
C = len(G[0])
# print(f"RxC {R}x{C}")


def solve(start, end, G):
    q = list()
    seen = set()
    q.append((0, start, (0, 0), 0))
    while q:
        d, (r, c), (cdr, cdc), n = heappop(q)

        if (r, c) == end:
            return d

        if (r, c, cdr, cdc, n) in seen:
            continue

        seen.add((r, c, cdr, cdc, n))

        if n < 3 and (cdr, cdc) != (0, 0):
            rr = r + cdr
            cc = c + cdc
            if 0 <= rr < R and 0 <= cc < C:
                heappush(q, (d+G[rr][cc], (rr, cc), (cdr, cdc), n+1))

        for (dr, dc) in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
            if (dr, dc) != (cdr, cdc) and (dr, dc) != (-cdr, -cdc):
                rr = r + dr
                cc = c + dc
                if 0 <= rr < R and 0 <= cc < C:
                    heappush(q, (d+G[rr][cc], (rr, cc), (dr, dc), 1))

    assert False, "got lost in maze"


def solve2(start, end, G):
    q = list()
    seen = set()
    q.append((0, start, (0, 0), 0))
    while q:
        d, (r, c), (cdr, cdc), n = heappop(q)

        if (r, c) == end:
            return d

        if (r, c, cdr, cdc, n) in seen:
            continue

        seen.add((r, c, cdr, cdc, n))

        if n < 10 and (cdr, cdc) != (0, 0):
            rr = r + cdr
            cc = c + cdc
            if 0 <= rr < R and 0 <= cc < C:
                heappush(q, (d+G[rr][cc], (rr, cc), (cdr, cdc), n+1))

        if n > 3 or (cdr, cdc) == (0, 0):
            for (dr, dc) in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
                if (dr, dc) != (cdr, cdc) and (dr, dc) != (-cdr, -cdc):
                    rr = r + dr
                    cc = c + dc
                    if 0 <= rr < R and 0 <= cc < C:
                        heappush(q, (d+G[rr][cc], (rr, cc), (dr, dc), 1))

    assert False, "got lost in maze"


T = solve((0, 0), (R-1, C-1), G)
T2 = solve2((0, 0), (R-1, C-1), G)
print(f"Tot {T} {T2}")
