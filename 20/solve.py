#!/usr/bin/env python3

import fileinput
from collections import deque

# counters
T = 0
T2 = 0
TL = TH = 0

R = dict()


for line in fileinput.input():
    l = line.strip()
    if not l:
        continue

    p = l.split(" -> ")
    n = p[0][1:]
    t = p[0][:1]

    s = False
    sl = [False]*10

    R[n] = {
        't': p[0][:1],
        'to': p[1].strip().split(", "),
        's': False,
        'from': dict()
    }

# setup connections
missing = set()
for rule in R.keys():
    for tr in R[rule]['to']:
        if tr in R:
            if R[tr]['t'] == '&':
                R[tr]['from'][rule] = False
        else:
            missing.add(tr)
for tr in missing:
    R[tr] = {'t': 'd', 'from': {}}


def reset():
    global R
    for rule in R.keys():
        R[rule]['s'] = False
        for f in R[rule]['from'].keys():
            R[rule]['from'][f] = False


def apply(pulse, rule, origin):
    global TL, TH, R

    if pulse:
        TH += 1
    else:
        TL += 1

    q = deque()

    if R[rule]['t'] == 'b':
        for tr in R[rule]['to']:
            # print("BC", rule, pulse, "to", tr)
            q.append((pulse, tr, rule))
    elif R[rule]['t'] == '%':
        if not pulse:
            R[rule]['s'] = not R[rule]['s']
            for tr in R[rule]['to']:
                # print("FF", rule, R[rule]['s'], "to", tr)
                q.append((R[rule]['s'], tr, rule))
    elif R[rule]['t'] == '&':
        R[rule]['from'][origin] = pulse
        np = not all(R[rule]['from'].values())
        for tr in R[rule]['to']:
            q.append((np, tr, rule))
    elif R[rule]['t'] == 'd':
        # drain/ouput
        pass
    else:
        assert False, ("unkown type", rule)

    return q


def push(pulse, rule, origin):
    q = deque()
    q.append((pulse, rule, origin))
    while q:
        (np, target, rule) = q.popleft()
        q.extend(apply(np, target, rule))


# # part 1
for i in range(1000):
    push(False, "roadcaster", "button")
T = TL*TH

# part 2
T2 = 1
# from instruction inspection, 4 regs with 9 bit values
registers = ['rg', 'pp', 'zp', 'sj']
for check in registers:
    reset()
    from_found = set()
    tot = 0
    for i in range(1, 1000000):
        push(False, "roadcaster", "button")

        for f in R[check]['from'].keys():
            if R[check]['from'][f] and f not in from_found:
                from_found.add(f)
                tot += i

        if len(from_found) == 9:
            T2 *= tot
            break

print(f"Tot {T} {T2}")
