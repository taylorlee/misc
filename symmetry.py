#something must be wrong!!! some not symmetric


# TODO
# look at states for H
# states with tau/4 rotations

import numpy as np
from numpy.linalg import eig

from fsm.fsm import FSM

Xb = np.array([
    [0,1],
    [1,0],
])
Yb = np.array([
    [0,-1j],
    [1j, 0],
])
Zb = np.array([
    [1,0],
    [0,-1],
])
Bloch = [Xb, Yb, Zb]

Xs = np.array([
    [1,0, 0],
    [0,-1, 0],
    [0,0, -1],
])
Ys = np.array([
    [-1,0,0],
    [0,1,0],
    [0,0,-1],
])
Zs = np.array([
    [-1,0,0],
    [0,-1,0],
    [0,0,1],
])
Cart = [Xs, Ys, Zs]

rot_names = {}
pole_names = {}

def splay(l):
    for x in l:
        print(x)

def main():
    #do_s3()
    do_bloch()

def set_rot_names(rots):
    for rot, name in zip(rots, 'XYZ'):
        rot_names[str(rot)] = name


def do_s3():
    set_rot_names(Cart)
    pole_names.clear()
    states = []
    for rot in [Zs]:
        pn = _build_pole_names(rot, imag=False)
        states += expand_states_cart(rot)
        pole_names.update(pn)
    title = 'S3'
    big_redo(states, Cart, title) 

def do_bloch():
    import ipdb; ipdb.set_trace()
    set_rot_names(Bloch)
    do_axis(Xb)
    do_axis(Yb)
    do_axis(Zb)

def do_axis(rot):
    pole_names.clear()
    pole_names.update(_build_pole_names(rot))
    states = expand_states_bloch(rot)
    title = fmt_pole(rot)
    big_redo(states, Bloch, title) 

def expand_states_cart(rot):
    a,b,c = eig(rot)[1]
    states = [a,b,c]
    for i in range(len(states)):
        x = states[i]
        states.append(-x)
    return states

def expand_states_bloch(rot):
    a,b = eig(rot)[1]
    states = [a,b]
    for i in range(len(states)):
        x = states[i]
        states.append(x*1j)
    for i in range(len(states)):
        x = states[i]
        states.append(-x)
    return states

def neutralize(num):
    if num.imag:
        return complex(num.real or 0, num.imag)
    return num.real or 0

def fmt_pole(pole):
    return pole_names[stringify_pole(pole)]

def stringify_pole(pole):
    return str(tuple(
        "{0:.10f}".format(neutralize(num))
        for num in pole
    ))

def fmt_rot(rot):
    return rot_names[str(rot)]

def big_redo(states, rots, title):
    fsm = FSM(pole_names.values(), directed=False)
    seen = set()
    for state in states:
        for rot in rots:
            subj = fmt_pole(state)
            verb = fmt_rot(rot)
            obj = fmt_pole(state @ rot)
            fmt = (subj, verb, obj)
            print('{} {} {}'.format(*fmt))
            if (subj, obj) in seen or (obj, subj) in seen:
                print('skip ^^')
                continue
            else:
                seen.add( (subj, obj) )
            fsm.transition(subj, obj, verb)

    fsm.save(name='bloch/{}-neato'.format(title), prog='neato')
    fsm.save(name='bloch/{}-dot'.format(title), prog='dot')

def _build_pole_names(rot, imag=True):
    letter = fmt_rot(rot).lower()
    itr = eig(rot)[1]
    pn = {}
    for i, pole in enumerate(itr):
        name = letter + str(i)
        idx = stringify_pole(pole)
        pn[idx] = name

        idx = stringify_pole(-pole)
        pn[idx] = '-' + name
        if imag: 
            idx = stringify_pole(pole*1j)
            pn[idx] = name + '*j'

            idx = stringify_pole(pole*-1j)
            pn[idx] = '-' + name + '*j'
    return pn

