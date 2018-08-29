#something must be wrong!!! some not symmetric
import numpy as np
from numpy.linalg import eig

from collections import defaultdict

from fsm.fsm import FSM


X = np.array([[0,1],[1,0]])
Y = np.array([[0,-1j],[1j, 0]])
Z = np.array([[1,0],[0,-1]])

rot_names = {
    str(X): 'X',
    str(Y): 'Y',
    str(Z): 'Z',
}

x0, x1 = eig(X)[1]
y0, y1 = eig(Y)[1]

def neutralize(num):
    if num.imag:
        return complex(num.real or 0, num.imag)
    return num.real

def fmt_pole(pole):
    return str(tuple(
        neutralize(num)
        for num in pole
    ))

pole_names = {}
for i, pole in enumerate([x0,x1]):
    name = 'x' + str(i)
    idx = fmt_pole(pole)
    pole_names[idx] = name

    idx = fmt_pole(-pole)
    pole_names[idx] = '-' + name
    
    idx = fmt_pole(pole*1j)
    pole_names[idx] = name + '*j'

    idx = fmt_pole(pole*-1j)
    pole_names[idx] = '-' + name + '*j'





def main():
    graph = dfs([x0,x1, -x0, -x1, x0*1j, x1*1j, -x0*1j, -x1*1j], [X,Y,Z])
    prettify(graph)


def dfs(unseen, rots):
    seen = []
    graph = defaultdict(set)
    while len(unseen) > 0:
        #print(seen, unseen, graph)
        node = unseen.pop()
        seen.append(node)
        for rot in rots:
            new = rot @ node
            for old in seen:
                if like(new, old):
                    graph[fmt_pole(node)].add((fmt_pole(old), str(rot)))
                    break
            else: #no break
                graph[fmt_pole(node)].add((fmt_pole(new), str(rot)))
                unseen.append(new)
              
    return graph

def prettify(graph):
    fsm = FSM(pole_names.values(), directed=False)
    for node, entries in graph.items():
        for adj, edge in entries:
            fmt = []
            for elem, namer in zip([node, edge, adj], [pole_names, rot_names, pole_names]):
                if str(elem) in rot_names:
                    fmt += [namer[str(elem)]]
                else:
                    fmt += [namer[elem]]

            print('{} {} {}'.format(*fmt))
            subj, verb, obj = fmt
            fsm.transition(subj, obj, verb)
    fsm.save(name='bloch')

def like(a, b):
    ratio = a/b
    same = ratio == 1
    flip = ratio == -1
    return same.all() or flip.all()
