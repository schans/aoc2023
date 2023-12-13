#!/usr/bin/env python3

import fileinput
import functools
from typing import Tuple

# counters
T = 0
T2 = 0


# def build_regexp(check: list[int]) -> str:
#     parts = []
#     for i in check:
#         parts.append(f"[#?]{{{i}}}")
#
#     return "^[\.\?]*" + "[\.\?]+".join(parts) + "[\.\?]*$"

@functools.cache
def do_count(row: str, check: Tuple[int]) -> int:
    if row == "":
        if len(check) == 0:
            return 1
        else:
            # still matches to do but no check
            return 0
    if len(check) == 0:
        if '#' in row:
            # can't match remaining #
            return 0
        else:
            # rest must be all dots, one option
            return 1

    acc = 0
    if row[0] in ".?":
        acc += do_count(row[1:], check)

    if row[0] in "#?":
        # fits in
        if check[0] <= len(row):
            # no dots breaking chain of #
            if '.' not in row[:check[0]]:
                # stop at end or with dot (or questionmark)
                if check[0] == len(row) or row[check[0]] != '#':
                    acc += do_count(row[check[0]+1:], check[1:])
    return acc


for line in fileinput.input():
    l = line.strip()
    if not l:
        continue

    p = l.split()

    T += do_count(p[0], tuple(int(x) for x in p[1].split(',')))
    T2 += do_count('?'.join([p[0]]*5), tuple(int(x) for x in p[1].split(','))*5)


print(f"Tot {T} {T2}")
