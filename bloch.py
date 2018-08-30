#something must be wrong!!! some not symmetric
import numpy as np
from numpy.linalg import eig

from collections import defaultdict

from fsm.fsm import FSM


X = np.array([[0,1],[1,0]])
Y = np.array([[0,-1j],[1j, 0]])
Z = np.array([[1,0],[0,-1]])
Rots = [X,Y,Z]

def main():
    do_axis(X)
    do_axis(Y)
    do_axis(Z)

def do_axis(rot):
    big_redo(rot, Rots)

def expand_states(rot):
    a,b = eig(rot)[1]
    states = [a,b]
    for i in range(len(states)):
        x = states[i]
        states.append(x*1j)
    for i in range(len(states)):
        x = states[i]
        states.append(-x)
    return states

def dfs(unseen, rots):
    seen = []
    graph = defaultdict(set)
    while len(unseen) > 0:
        node = unseen.pop()
        seen.append(node)
        for rot in rots:
            new = rot @ node
            for old in seen:
                if like(new, old):
                    graph[fmt_pole(node)].add((fmt_pole(old), fmt_rot(rot)))
                    break
            else: #no break
                graph[fmt_pole(node)].add((fmt_pole(new), fmt_rot(rot)))
                unseen.append(new)
            print(graph)
              
    return graph

def neutralize(num):
    if num.imag:
        return complex(num.real or 0, num.imag)
    return num.real

def fmt_pole(pole):
    return pole_names[stringify_pole(pole)]

def stringify_pole(pole):
    return str(tuple(
        neutralize(num)
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

    fsm.save(name='bloch-{}'.format(fmt_rot(axis)), prog='neato')

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

def prettify(graph):
    fsm = FSM(pole_names.values(), directed=False)
    for node, entries in graph.items():
        for adj, edge in entries:
            fmt = []
            for elem, namer in zip([node, edge, adj], [pole_names, rot_names, pole_names]):
                fmt += [elem]

            print('{} {} {}'.format(*fmt))
            subj, verb, obj = fmt
            fsm.transition(subj, obj, verb)
    fsm.save(name='bloch')

def like(a, b):
    ratio = a/b
    same = ratio == 1
    flip = ratio == -1
    return same.all() or flip.all()

rot_names = {
    str(X): 'X',
    str(Y): 'Y',
    str(Z): 'Z',
}
pole_names = build_pole_names()


