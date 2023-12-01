#!/usr/bin/env python3

import fileinput
from os import truncate

# counters
T = 0
T2 = 0
N = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']


def get_num(line: str) -> int:
    d1 = ''
    d2 = '0'
    for c in line:
        if str(c).isdigit():
            if not d1:
                d1 = str(c)
                d2 = str(c)
            else:
                d2 = str(c)
    return int(d1+d2)


for line in fileinput.input():
    l = line.strip()
    if not l:
        continue

    nl = ""
    for i, c in enumerate(line):
        r = False
        for k, n in enumerate(N):
            if line[i:].startswith(n):
                nl += str(k)
                r = True
        if not r:
            nl += c
    T += get_num(line)
    T2 += get_num(nl)

print(f"Tot {T} {T2}")
