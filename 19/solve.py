#!/usr/bin/env python3

import fileinput

# counters
T = 0
T2 = 0
W = dict()
R = list()

inwf = True
for line in fileinput.input():
    l = line.strip()
    if not l:
        inwf = False
        continue

    if inwf:
        n, r = l.split('{')
        r = r[:-1]
        W[n] = r.split(',')
    else:
        ps = l[1:-1].split(',')
        d = dict()
        for p in ps:
            d[p[0:1]] = int(p[2:])
        R.append(d)


def apply(v, wf):
    x = v['x']
    m = v['m']
    a = v['a']
    s = v['s']
    for r in W[wf]:
        p = r.split(':')
        if len(p) == 1:
            # end rule
            return p[0]
        elif len(p) == 2:
            # wf rule
            if eval(p[0]):
                return p[1]
        else:
            assert False, ("invalid rule", wf, r)
    assert False, ("ran out of rules", wf, v)


# part 1
for r in R:
    t = 'in'
    while t not in ["A", "R"]:
        t = apply(r, t)
    if t == "A":
        T += r['x'] + r['m'] + r['a'] + r['s']


# part 2
def get_options(wf, xr, mr, ar, sr):
    if wf == 'A':
        return (xr[1] - xr[0])*(mr[1]-mr[0])*(ar[1]-ar[0])*(sr[1]-sr[0])
    elif wf == 'R':
        return 0

    cnt = 0
    for r in W[wf]:
        p = r.split(':')

        # end rule
        if len(p) == 1:
            cnt += get_options(p[0], xr, mr, ar, sr)

        # wf rule -> split() -> if False, continue, if True, end or step into
        elif len(p) == 2:
            val = int(p[0][2:])

            if p[0][0] == 'x':
                (vmin, vmax) = xr
                if '<' in p[0]:
                    # true part
                    nxr = (min(val, vmin), min(val, vmax))
                    cnt += get_options(p[1], nxr, mr, ar, sr)
                    # false part
                    xr = (max(val, vmin), max(val, vmax))
                elif '>' in p[0]:
                    # true part
                    nxr = (max(val+1, vmin), max(val+1, vmax))
                    cnt += get_options(p[1], nxr, mr, ar, sr)
                    # false part
                    xr = (min(val+1, vmin), min(val+1, vmax))
            elif p[0][0] == 'm':
                (vmin, vmax) = mr
                if '<' in p[0]:
                    # true part
                    nmr = (min(val, vmin), min(val, vmax))
                    cnt += get_options(p[1], xr, nmr, ar, sr)
                    # false part
                    mr = (max(val, vmin), max(val, vmax))
                elif '>' in p[0]:
                    # true part
                    nmr = (max(val+1, vmin), max(val+1, vmax))
                    cnt += get_options(p[1], xr, nmr, ar, sr)
                    # false part
                    mr = (min(val+1, vmin), min(val+1, vmax))
            elif p[0][0] == 'a':
                (vmin, vmax) = ar
                if '<' in p[0]:
                    # true part
                    nar = (min(val, vmin), min(val, vmax))
                    cnt += get_options(p[1], xr, mr, nar, sr)
                    # false part
                    ar = (max(val, vmin), max(val, vmax))
                elif '>' in p[0]:
                    # true part
                    nar = (max(val+1, vmin), max(val+1, vmax))
                    cnt += get_options(p[1], xr, mr, nar, sr)
                    # false part
                    ar = (min(val+1, vmin), min(val+1, vmax))
            elif p[0][0] == 's':
                (vmin, vmax) = sr
                if '<' in p[0]:
                    # true part
                    nsr = (min(val, vmin), min(val, vmax))
                    cnt += get_options(p[1], xr, mr, ar, nsr)
                    # false part
                    sr = (max(val, vmin), max(val, vmax))
                elif '>' in p[0]:
                    # true part
                    nsr = (max(val+1, vmin), max(val+1, vmax))
                    cnt += get_options(p[1], xr, mr, ar, nsr)
                    # false part
                    sr = (min(val+1, vmin), min(val+1, vmax))
            else:
                assert False, ("unkown equality", p[0])
        else:
            assert False, ("invalid rule", wf, r)

    return cnt


T2 = get_options('in', (1, 4001), (1, 4001), (1, 4001), (1, 4001))


print(f"Tot {T} {T2}")
