#!/usr/bin/env python3

from pprint import pprint
import fileinput
from heapq import heappop, heappush
from collections import deque

# counters
T = T2 = 0

G = [[c for c in l.strip()] for l in fileinput.input()]
# R = len(G)
# C = len(G[0])
# print(f"RxC {R}x{C}")


def get_start(G):
    for c in range(len(G[0])):
        if G[0][c] == '.':
            return (0, c)


def get_end(G):
    for c in range(len(G[0])):
        if G[len(G)-1][c] == '.':
            return (len(G)-1, c)


# part 1, brute force dfs (slow)
def solve(start, end, G):
    R = len(G)
    C = len(G[0])
    q = deque()
    q.append((start, 0, set()))
    ns = set()
    while q:
        (r, c), n, steps = q.popleft()

        if (r, c) == end:
            ns.add(n)
            continue

        if (r, c) in steps:
            continue
        steps.add((r, c))

        if G[r][c] == '>':
            rr = r + 0
            cc = c + 1
            if 0 <= rr < R and 0 <= cc < C and G[rr][cc] != '#':
                q.append(((rr, cc), n+1, steps))
        elif G[r][c] == 'v':
            rr = r + 1
            cc = c + 0
            if 0 <= rr < R and 0 <= cc < C and G[rr][cc] != '#':
                q.append(((rr, cc), n+1, steps))
        else:
            for (dr, dc) in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
                rr = r + dr
                cc = c + dc
                if 0 <= rr < R and 0 <= cc < C and G[rr][cc] != '#':
                    q.append(((rr, cc), n+1, steps.copy()))

    return max(ns)


def get_points(G):
    R = len(G)
    C = len(G[0])
    points = set()
    for r in range(1, len(G)-1):
        for c in range(1, len(G[0])-1):
            p = 0
            if G[r][c] != '#':
                for (dr, dc) in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
                    rr = r + dr
                    cc = c + dc
                    if 0 <= rr < R and 0 <= cc < C and G[rr][cc] and G[rr][cc] != '#':
                        p += 1
                # more than 2 paths is split
                if p > 2:
                    points.add((r, c))
    return points


def get_graph(P, G):
    R = len(G)
    C = len(G[0])

    # init
    graph = dict()
    for p in P:
        graph[p] = dict()

    # find edges
    for p in P:
        (sr, sc) = p
        q = deque()
        seen = set()
        q.append((sr, sc, 0))
        seen.add((sr, sc))

        while q:
            r, c, n = q.pop()

            if n != 0 and (r, c) in P:
                # biderect
                graph[(sr, sc)][(r, c)] = n
                graph[(r, c)][(sr, sc)] = n
                continue

            for (dr, dc) in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
                rr = r + dr
                cc = c + dc
                if 0 <= rr < R and 0 <= cc < C and G[rr][cc] and G[rr][cc] != '#' and not (rr, cc) in seen:
                    q.append((rr, cc, n+1))
                    seen.add((rr, cc))

    return graph


def solve2(start, end, graph):
    q = deque()
    q.append((start, 0, {start}))
    ends = list()

    while q:
        p, n, visited = q.popleft()
        if p == end:
            ends.append(n)
            continue

        for np in graph[p]:
            if not np in visited:
                nv = visited.copy()
                nv.add((np))
                q.append((np, n+graph[p][np], nv))

    return max(ends)


# part 1
start = get_start(G)
end = get_end(G)
T = solve(start, end, G)

# part 2
points = get_points(G)
points.add(start)
points.add(end)
graph = get_graph(points, G)
T2 = solve2(start, end, graph)

print(f"Tot {T} {T2}")
