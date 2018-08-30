#something must be wrong!!! some not symmetric
import numpy as np
from numpy.linalg import eig

from fsm.fsm import FSM

X = np.array([[0,1],[1,0]])
Y = np.array([[0,-1j],[1j, 0]])
Z = np.array([[1,0],[0,-1]])



Z = np.array([
    [-1,0,0],
    [0,-1,0],
    [0,0,1],
])
Y = np.array([
    [-1,0,0],
    [0,1,0],
    [0,0,-1],
])

X= np.array([
    [1,0, 0],
    [0,-1, 0],
    [0,0, -1],
])

Rots = [X,Y,Z]

#TODO: S3 has issues!
rot_names = {
    str(X): 'EW',
    str(Y): 'NS',
    str(Z): 'TB',
}
pole_names = {}



def splay(l):
    for x in l:
        print(x)

def main():
    do_axis(X)
    do_axis(Y)
    do_axis(Z)

def do_axis(rot):
    pole_names.clear()
    pole_names.update(_build_pole_names(rot))
    big_redo(rot, Rots)

def expand_states(rot):
    #TODO: back to a,b
    a,b,c = eig(rot)[1]
    states = [a,b,c]
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

def big_redo(axis, rots):
    fsm = FSM(pole_names.values(), directed=False)
    states = expand_states(axis)
    seen = set()
    for state in states:
        for rot in rots:
            subj = fmt_pole(state)
            verb = fmt_rot(rot)
            obj = fmt_pole(state @ rot)
            fmt = (subj, verb, obj)
            if (subj, obj) in seen or (obj, subj) in seen:
                continue
            else:
                seen.add( (subj, obj) )
            print('{} {} {}'.format(*fmt))
            fsm.transition(subj, obj, verb)

    fsm.save(name='bloch/{}-neato'.format(fmt_rot(axis)), prog='neato')
    fsm.save(name='bloch/{}-dot'.format(fmt_rot(axis)), prog='dot')

def build_pole_names():
    ret = {}
    for rot in Rots:
        ret.update(_build_pole_names(rot))
    return ret

def _build_pole_names(rot):
    letter = fmt_rot(rot).lower()
    itr = eig(rot)[1]
    pn = {}
    for i, pole in enumerate(itr):
        name = letter + str(i)
        idx = stringify_pole(pole)
        pn[idx] = name

        idx = stringify_pole(-pole)
        pn[idx] = '-' + name
        
        idx = stringify_pole(pole*1j)
        pn[idx] = name + '*j'

        idx = stringify_pole(pole*-1j)
        pn[idx] = '-' + name + '*j'
    return pn

def like(a, b):
    ratio = a/b
    same = ratio == 1
    flip = ratio == -1
    return same.all() or flip.all()
