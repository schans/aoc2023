#!/usr/bin/env python3

import fileinput

# counters
T = T2 = 0

G = [[c for c in l.strip()] for l in fileinput.input()]
R = len(G)
C = len(G[0])


def get_start(G):
    for r in range(len(G)):
        for c in range(len(G[0])):
            if G[r][c] == 'S':
                return (r, c)

    return (-1, -1)


def solve(start, max_step, G):
    seen_odd = set()
    seen_even = set()
    new_odd = set()
    new_even = set()
    new_even.add(start)
    for i in range(max_step):

        if i % 2:
            new_even.clear()
            for (r, c) in new_odd:
                for (dr, dc) in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
                    rr = r + dr
                    cc = c + dc
                    if 0 <= rr < R and 0 <= cc < C and G[rr][cc] != '#' and not (rr, cc) in seen_even:
                        new_even.add((rr, cc))
                        seen_even.add((rr, cc))

        else:
            new_odd.clear()
            for (r, c) in new_even:
                for (dr, dc) in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
                    rr = r + dr
                    cc = c + dc
                    if 0 <= rr < R and 0 <= cc < C and G[rr][cc] != '#' and not (rr, cc) in seen_odd:
                        new_odd.add((rr, cc))
                        seen_odd.add((rr, cc))

    if max_step % 2:
        return len(seen_odd)
    else:
        return len(seen_even)


# part 1
start = get_start(G)
print(f"RxC {R}x{C} {start=}")
T = solve(start, 64, G)

# part 2
steps = 26501365
max_grid_dist = steps//R
rest_steps = steps % R
print(f"{max_grid_dist=} {rest_steps=}")

"""
observations from input:
- grid a sqare and odd sized
- start is in middle
- all edges are dots
- from start, straight, up, down, left, right are dots (cross through S)
- steps stop at last grid edge
"""
assert R == C, "square"
assert start[0] == (R-1)/2, "start in middle"
assert start[1] == (R-1)/2, "start in middle"
assert rest_steps == (R-1)/2, "exact end of grid reached"
assert all('#' != G[x][0] and '#' != G[0][x] for x in range(R)), "edges"
assert all('#' != G[x][C-1] and '#' != G[R-1][x] for x in range(R)), "edges"
assert all('#' != G[x][start[1]] and '#' != G[start[0]][x] for x in range(R)), "cross"


def solve_inf(start, max_step, G):
    seen_odd = set()
    seen_even = set()
    new_odd = set()
    new_even = set()
    new_even.add(start)
    for i in range(max_step):

        if i % 2:
            new_even.clear()
            for (r, c) in new_odd:
                for (dr, dc) in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
                    rr = r + dr
                    cc = c + dc
                    if G[rr % R][cc % C] != '#' and not (rr, cc) in seen_even:
                        new_even.add((rr, cc))
                        seen_even.add((rr, cc))

        else:
            new_odd.clear()
            for (r, c) in new_even:
                for (dr, dc) in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
                    rr = r + dr
                    cc = c + dc
                    if G[rr % R][cc % C] != '#' and not (rr, cc) in seen_odd:
                        new_odd.add((rr, cc))
                        seen_odd.add((rr, cc))

    if max_step % 2:
        return len(seen_odd)
    else:
        return len(seen_even)


def get_odd_even_count(max_grid_dist):
    """
    grid layout in odd-even

         0 1 2 3 4 5 6 7 8 9 0
     b a S a b b a S a b b a S a b
     --------- --------- ---------
        even      odd      even

    full grids layout

                E
              E O E
            E O E O E
          E O E O E O E
            E O E O E
              E O E
                E
    """
    max_grid_dist -= 1  # easier calc
    odds = evens = 0
    for i in range(1, max_grid_dist+1):
        if max_grid_dist % 2:
            odds += i - 1
            evens += i
        else:
            odds += i
            evens += i - 1

    # top and bottom
    evens *= 2
    odds *= 2

    # middle row
    if max_grid_dist % 2:
        odds += max_grid_dist
        evens += max_grid_dist + 1
    else:
        odds += max_grid_dist + 1
        evens += max_grid_dist

    print(f"{odds=} {evens=}")
    return (odds, evens)


"""
calc full odd and even filled
"""
full_even = solve(start, 2*R, G)
full_odd = solve(start, 2*R+1, G)
print(f"{full_odd=} {full_even=}")

# rest_steps = 65

"""
calc corners 
fille from top bottom left and right
"""
corners = 0
corners += solve((0, 65), R - 1, G)  # bottom
corners += solve((R-1, 65), R - 1, G)  # top
corners += solve((65, 0), C-1, G)  # right
corners += solve((65, C-1), C-1, G)  # left
print(f"{corners=}")


"""
calc quads of small and large sides
"""
edges2 = edges4 = 0
for i in range(2, 5, 2):
    n = R * i + 65
    # print(i, n, solve_inf(start, n, G))
    if i == 2:
        # 4 * corner
        # 1 * odd (middle)
        # 4 * even (around)
        # 4* i = 8 * small piece
        # 4* (i -1) = 4 large piece
        (no, ne) = get_odd_even_count(i)
        edges2 = solve_inf(start, n, G) - no * full_odd - ne * full_even - corners
        print(f"{edges2=}")
    if i == 4:
        # 4 * corner
        # 9 * odd (middle)
        # 16 * even (around)
        # 4* i = 16 * small piece
        # 4 * (i-1) = 12 large piece
        (no, ne) = get_odd_even_count(i)
        edges4 = solve_inf(start, n, G) - no * full_odd - ne * full_even - corners
        print(f"{edges4=}")
        pass

"""
2*small4 + large4 = edges2
4*small4 + 3 large4 = edges4
large4 = edges4 - edges2

large4 = 25725
small4 = 3769
"""
large4 = edges4 - 2*edges2
small4 = (edges2 - large4)//2
print(f"{small4=}  {large4=}")

# verify
i = 8
(no, ne) = get_odd_even_count(i)
t = no * full_odd + ne * full_even
t += corners
t += i*small4 + (i-1) * large4
assert solve_inf(start, R*i+65, G) == t


i = max_grid_dist
(no, ne) = get_odd_even_count(i)
T2 = no * full_odd + ne * full_even
T2 += corners
T2 += i*small4 + (i-1) * large4

print(f"Tot {T} {T2}")
